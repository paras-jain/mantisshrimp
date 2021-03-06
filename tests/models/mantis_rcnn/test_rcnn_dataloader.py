from mantisshrimp.imports import Tensor, tensor, first
from mantisshrimp import *


def test_mask_rcnn_dataloader(records):
    dataset = Dataset(records)
    dl = MantisMaskRCNN.dataloader(dataset, batch_size=3)
    xb, yb = first(dl)
    assert len(xb) == 3
    assert len(yb) == 3

    x = xb[0]
    assert x.shape == (3, 427, 640)
    assert isinstance(x, Tensor)

    y = yb[0]
    assert y["image_id"] == 0
    assert allequal([isinstance(o, Tensor) for o in y.values()])
    assert (
        y["labels"] == tensor([6, 1, 1, 1, 1, 1, 1, 1, 31, 31, 1, 3, 31, 1, 31, 31])
    ).all()
    assert (y["boxes"][0] == tensor([0.0000, 73.8900, 416.4400, 379.0200])).all()
    assert y["masks"].shape == (16, 427, 640)
    assert not (y["masks"] == 0).all()
    assert allequal(lmap(len, [y["labels"], y["boxes"], y["masks"]]))
