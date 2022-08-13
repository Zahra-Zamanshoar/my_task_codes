from enum import Enum
from typing import Sequence, Union
import numpy as np
# from deep_utils.utils.logging_utils.logging_utils import log_print, value_error_log
# from deep_utils import deep_utils


class Point:
    class PointSource(Enum):
        Torch = "Torch"
        TF = "TF"
        CV = "CV"
        Numpy = "Numpy"

    @staticmethod
    def point2point(
            point,
            in_source,
            to_source,
            in_relative=None,
            to_relative=None,
            shape=None,
            shape_source=None,
    ):
        if point is None or len(point) == 0:
            pass
        elif isinstance(point[0], (tuple, list, np.ndarray)):
            point = [
                Point._point2point(
                    p,
                    in_source=in_source,
                    to_source=to_source,
                    in_relative=in_relative,
                    to_relative=to_relative,
                    shape=shape,
                    shape_source=shape_source,
                )
                for p in point
            ]
        else:
            point = Point._point2point(
                point,
                in_source=in_source,
                to_source=to_source,
                in_relative=in_relative,
                to_relative=to_relative,
                shape=shape,
                shape_source=shape_source,
            )
        return point

    @staticmethod
    def _point2point(
            point,
            in_source : Union[str, PointSource],
            to_source : Union[str, PointSource],
            in_relative=None,
            to_relative=None,
            shape=None,
            shape_source=None,
    ):
        if isinstance(in_source, Point.PointSource):
            in_source = in_source.value
        if isinstance(to_source, Point.PointSource):
            to_source = to_source.value
        in_source =in_source.lower()
        to_source =to_source.lower()

        if (
                in_source in [Point.PointSource.Torch.value.lower(),
                              Point.PointSource.CV.value.lower()]
                and to_source in [Point.PointSource.TF.value.lower(), Point.PointSource.Numpy.value.lower()]
        ) or (
                in_source in [Point.PointSource.TF.value.lower(),
                              Point.PointSource.Numpy.value.lower()]
                and to_source in [Point.PointSource.Torch.value, Point.PointSource.CV.value.lower()]
        ):
            point = (point[1], point[0])
        elif (
                (in_source is None and to_source is None)
                or in_source == to_source
                or (
                        in_source in [Point.PointSource.Torch.value.lower(),
                                      Point.PointSource.CV.value.lower()]
                        and to_source
                        in [Point.PointSource.CV.value, Point.PointSource.Torch.value.lower()]
                )
                or (
                        in_source in [Point.PointSource.TF.value.lower(),
                                      Point.PointSource.Numpy.value.lower()]
                        and to_source
                        in [Point.PointSource.TF.value.lower(), Point.PointSource.Numpy.value.lower()]
                )
        ):
            pass
        else:
            raise Exception(
                f"Conversion form {in_source} to {to_source} is not Supported."
                f" Supported types: {Box._get_enum_names(Point.PointSource)}"
            )
        if to_source is not None and shape_source is not None and shape is not None:
            img_w, img_h = Point.point2point(
                shape, in_source=shape_source, to_source=to_source
            )
            if not in_relative and to_relative:
                p1, p2 = point
                point = [p1 / img_w, p2 / img_h]
            elif in_relative and not to_relative:
                p1, p2 = point
                point = [p1 * img_w, p2 * img_h]
        return point

    @staticmethod
    def _put_point(
            img,
            point,
            radius,
            color=(0, 255, 0),
            thickness=None,
            lineType=None,
            shift=None,
            in_source="Numpy",
    ):
        import cv2

        if not isinstance(point, int):
            point = (int(point[0]), int(point[1]))
        point = Point.point2point(point, in_source=in_source, to_source="CV")
        return cv2.circle(img, point, radius, color, thickness, lineType, shift)

    @staticmethod
    def put_point(
            img,
            point,
            radius,
            color=(0, 255, 0),
            thickness=None,
            lineType=None,
            shift=None,
            in_source="Numpy",
    ):
        if point is None or len(point) == 0:
            pass
        elif isinstance(point[0], (tuple, list, np.ndarray)):
            for p in point:
                img = Point._put_point(
                    img, p, radius, color, thickness, lineType, shift, in_source
                )
        else:
            img = Point._put_point(
                img, point, radius, color, thickness, lineType, shift, in_source
            )
        return img

    @staticmethod
    def sort_points(pts: Union[list, tuple]):
        """
        Sort a list of 4 points based on upper-left, upper-right, down-right, down-left
        :param pts:
        :return:
        """
        top_points = sorted(pts, key=lambda l: l[0])[:2]
        top_left = min(top_points, key=lambda l: l[1])
        top_right = max(top_points, key=lambda l: l[1])
        pts.remove(top_left)
        pts.remove(top_right)
        down_left = min(pts, key=lambda l: l[1])
        down_right = max(pts, key=lambda l: l[1])
        return top_left, top_right, down_right, down_left