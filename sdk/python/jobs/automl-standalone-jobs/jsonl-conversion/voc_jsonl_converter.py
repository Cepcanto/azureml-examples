from base_jsonl_converter import JSONLConverter
import os
import xml.etree.ElementTree as ET
import numpy as np
import PIL.Image as Image
from simplification.cutil import simplify_coords
from skimage import measure

class VOCJSONLConverter(JSONLConverter):
    def __init__(self, base_url, xml_dir, mask_dir = None):
        super().__init__(base_url=base_url)
        self.xml_dir = xml_dir
        self.mask_dir = mask_dir

    def convert_mask_to_polygon(
        self,
        mask,
        max_polygon_points=100,
        score_threshold=0.5,
        max_refinement_iterations=25,
        edge_safety_padding=1,
    ):
        """Convert a numpy mask to a polygon outline in normalized coordinates.

        :param mask: Pixel mask, where each pixel has an object (float) score in [0, 1], in size ([1, height, width])
        :type: mask: <class 'numpy.array'>
        :param max_polygon_points: Maximum number of (x, y) coordinate pairs in polygon
        :type: max_polygon_points: Int
        :param score_threshold: Score cutoff for considering a pixel as in object.
        :type: score_threshold: Float
        :param max_refinement_iterations: Maximum number of times to refine the polygon
        trying to reduce the number of pixels to meet max polygon points.
        :type: max_refinement_iterations: Int
        :param edge_safety_padding: Number of pixels to pad the mask with
        :type edge_safety_padding: Int
        :return: normalized polygon coordinates
        :rtype: list of list
        """
        # Convert to numpy bitmask
        mask = mask[0]
        mask_array = np.array((mask > score_threshold), dtype=np.uint8)
        image_shape = mask_array.shape

        # Pad the mask to avoid errors at the edge of the mask
        embedded_mask = np.zeros(
            (
                image_shape[0] + 2 * edge_safety_padding,
                image_shape[1] + 2 * edge_safety_padding,
            ),
            dtype=np.uint8,
        )
        embedded_mask[
            edge_safety_padding : image_shape[0] + edge_safety_padding,
            edge_safety_padding : image_shape[1] + edge_safety_padding,
        ] = mask_array

        # Find Image Contours
        contours = measure.find_contours(embedded_mask, 0.5)
        simplified_contours = []

        for contour in contours:

            # Iteratively reduce polygon points, if necessary
            if max_polygon_points is not None:
                simplify_factor = 0
                while (
                    len(contour) > max_polygon_points
                    and simplify_factor < max_refinement_iterations
                ):
                    contour = simplify_coords(contour, simplify_factor)
                    simplify_factor += 1

            # Convert to [x, y, x, y, ....] coordinates and correct for padding
            unwrapped_contour = [0] * (2 * len(contour))
            unwrapped_contour[::2] = np.ceil(contour[:, 1]) - edge_safety_padding
            unwrapped_contour[1::2] = np.ceil(contour[:, 0]) - edge_safety_padding

            simplified_contours.append(unwrapped_contour)

        return self._normalize_contour(simplified_contours, image_shape)


    def _normalize_contour(self, contours, image_shape):

        height, width = image_shape[0], image_shape[1]

        for contour in contours:
            contour[::2] = [x * 1.0 / width for x in contour[::2]]
            contour[1::2] = [y * 1.0 / height for y in contour[1::2]]

        return contours


    def binarise_mask(self, mask_fname):

        mask = Image.open(mask_fname)
        mask = np.array(mask)
        # instances are encoded as different colors
        obj_ids = np.unique(mask)
        # first id is the background, so remove it
        obj_ids = obj_ids[1:]

        # split the color-encoded mask into a set of binary masks
        binary_masks = mask == obj_ids[:, None, None]
        return binary_masks


    def parsing_mask(self, mask_fname):

        # For this particular dataset, initially each mask was merged (based on binary mask of each object)
        # in the order of the bounding boxes described in the corresponding PASCAL VOC annotation file.
        # Therefore, we have to extract each binary mask which is in the order of objects in the annotation file.
        # https://github.com/microsoft/computervision-recipes/blob/master/utils_cv/detection/dataset.py
        binary_masks = self.binarise_mask(mask_fname)
        polygons = []
        for bi_mask in binary_masks:

            if len(bi_mask.shape) == 2:
                bi_mask = bi_mask[np.newaxis, :]
            polygon = self.convert_mask_to_polygon(bi_mask)
            polygons.append(polygon)

        return polygons

    def convert(self):
        json_line_sample = {
            "image_url": self.base_url,
            "image_details": {"format": None, "width": None, "height": None},
            "label": [],
        }

        for i, filename in enumerate(os.listdir(self.xml_dir)):
            if not filename.endswith(".xml"):
                print(f"Skipping unknown file: {filename}")
                continue

            annotation_filename = os.path.join(self.xml_dir, filename)
            print(f"Parsing {annotation_filename}")

            root = ET.parse(annotation_filename).getroot()
            width = int(root.find("size/width").text)
            height = int(root.find("size/height").text)

            # convert mask into polygon
            if self.mask_dir is not None:
                mask_fname = os.path.join(self.mask_dir, filename[:-4] + ".png")
                polygons = self.parsing_mask(mask_fname)

            labels = []
            for index, object in enumerate(root.findall("object")):
                name = object.find("name").text
                isCrowd = int(object.find("difficult").text)
                if self.mask_dir is None: # do object detection
                    xmin = object.find("bndbox/xmin").text
                    ymin = object.find("bndbox/ymin").text
                    xmax = object.find("bndbox/xmax").text
                    ymax = object.find("bndbox/ymax").text
                
                    labels.append(
                        {
                            "label": name,
                            "topX": float(xmin) / width,
                            "topY": float(ymin) / height,
                            "bottomX": float(xmax) / width,
                            "bottomY": float(ymax) / height,
                            "isCrowd": isCrowd,
                        }
                    )
                else:
                    labels.append(
                        {
                            "label": name,
                            "bbox": "null",
                            "isCrowd": isCrowd,
                            "polygon": polygons[index]
                        }
                    )
            # build the jsonl file
            image_filename = root.find("filename").text
            _, file_extension = os.path.splitext(image_filename)
            json_line = dict(json_line_sample)
            json_line["image_url"] = os.path.join(json_line["image_url"],image_filename)
            json_line["image_details"]["format"] = file_extension[1:]
            json_line["image_details"]["width"] = width
            json_line["image_details"]["height"] = height
            json_line["label"] = labels

            self.jsonl_data.append(json_line)
        return self.jsonl_data