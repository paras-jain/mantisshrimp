__all__ = ["parser", "PetsXmlParser", "PetsMaskParser", "PetsMaskFile"]

from mantisshrimp.imports import *
from mantisshrimp.core import *
from mantisshrimp.parsers import *
from mantisshrimp.datasets.pets import CATEGORIES


def parser(data_dir: Path, mask=False):
    parser = PetsXmlParser(
        annotations_dir=data_dir / "annotations/xmls",
        images_dir=data_dir / "images",
        categories=CATEGORIES,
    )

    if mask:
        mask_parser = PetsMaskParser(data_dir / "annotations/trimaps")
        parser = CombinedParser(parser, mask_parser)

    return parser


class PetsXmlParser(VocXmlParser):
    def label(self, o) -> List[int]:
        name = re.findall(r"^(.*)_\d+$", o.stem)[0]
        return [self.category2id[name]]


class PetsMaskParser(VocMaskParser):
    def mask(self, o) -> List[Mask]:
        return [PetsMaskFile(o)]


@dataclass
class PetsMaskFile(VocMaskFile):
    """ Extension of `MaskFile` for Pets masks.
    Invert 0s and 1s in the mask (the background is orignally 1 in the pets masks)
    Removes the color pallete and optionally drops void pixels.

    Args:
          drop_void (bool): drops the void pixels, which should have the value 255.
    """

    def to_mask(self, h, w) -> MaskArray:
        mask = super().to_mask(h=h, w=w)
        mask.data = 1 - mask.data
        return mask