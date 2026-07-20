from .base_extractor import BaseExtractor

class ImageExtractor(BaseExtractor):
    def extract(self, page):
        """
        Extracts images from a PDF page.

        Args:
            page (fitz.Page): The PDF page from which to extract images.
        """
        images = []
        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = page.get_image(xref)
            image_bytes = base_image["image"]
            images.append({
                "id": f"page_{page.number}_image_{img_index}",
                "image_bytes": image_bytes,
                "width": base_image["width"],
                "height": base_image["height"],
            })
        return images