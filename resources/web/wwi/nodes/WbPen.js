import WbSolid from './WbSolid.js';
import {array3Pointer, arrayXPointerFloat} from './utils/utils.js';
import WbRay from './utils/WbRay.js';
import WbVector3 from './utils/WbVector3.js';

import WbWrenRenderingContext from '../wren/WbWrenRenderingContext.js';
import WbWrenShaders from '../wren/WbWrenShaders.js';

export default class WbPen extends WbSolid {
  constructor(id, translation, scale, rotation, inkColor, inkDensity, leadSize, write, maxDistance) {
    super(id, translation, scale, rotation);
    this.inkColor = inkColor;
    this.inkDensity = inkDensity;
    this.leadSize = leadSize;
    this.write = write;
    this.maxDistance = maxDistance;
  }

  createWrenObjects() {
    super.createWrenObjects();
    this.prePhysicsStep();
  }

  prePhysicsStep() {
    if (this.maxDistance <= 0.0)
      this.maxDistance = Infinity;

    if (this.write) {
      // find shape/texture that intersects the ray
      const m = super.matrix();
      const globalDirection = m.sub3x3MatrixDot(new WbVector3(0, 0, -1));
      const ray = new WbRay(m.translation(), globalDirection);
    //   double distance;
    //   const WbShape *shape = WbNodeUtilities::findIntersectingShape(ray, maxDistance, distance);
    //
    //   if (shape && WbPaintTexture::isPaintable(shape)) {
    //     if (!mLastPaintTexture || shape != mLastPaintTexture->shape())
    //       mLastPaintTexture = WbPaintTexture::paintTexture(shape);
    //
    //     if (mLastPaintTexture)
    //       mLastPaintTexture->paint(ray, mLeadSize->value(), mInkColor->value(), mInkDensity->value());
    //   }
    }
  }
}
