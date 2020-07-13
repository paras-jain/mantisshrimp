from mantisshrimp.imports import *
from mantisshrimp.utils import *
from mantisshrimp.core import *
from mantisshrimp.models.rcnn.faster_rcnn.prediction import (
    convert_raw_prediction as faster_convert_raw_prediction,
)


@torch.no_grad()
def predict(
    model: nn.Module,
    batch: List[torch.Tensor],
    detection_threshold: float = 0.5,
    mask_threshold: float = 0.5,
    device: Optional[torch.device] = None,
):
    model.eval()
    device = device or model_device(model)
    images = [img.to(device) for img in batch]

    raw_preds = model(images)
    preds = [
        convert_raw_prediction(
            raw_pred=raw_pred,
            detection_threshold=detection_threshold,
            mask_threshold=mask_threshold,
        )
        for raw_pred in raw_preds
    ]

    return preds


def convert_raw_prediction(
    raw_pred: dict, detection_threshold: float, mask_threshold: float
):
    preds = faster_convert_raw_prediction(
        raw_pred=raw_pred, detection_threshold=detection_threshold
    )

    above_threshold = preds["above_threshold"]
    masks_probs = raw_pred["masks"][above_threshold]
    masks_probs = masks_probs.detach().cpu().numpy()
    # convert probabilities to 0 or 1 based on mask_threshold
    masks = masks_probs > mask_threshold
    masks = MaskArray(masks.squeeze(1))

    return {"masks": masks, **preds}