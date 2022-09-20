import WbVector3 from './WbVector3.js';

export default class WbBoundingSphere {
  constructor(owner, center = new WbVector3(), radius = 0) {
    this.center = center;
    this.radius = radius;
  }

  setOwnerSizeChanged() {
    if (this.geomOwner || this.skinOwner)
      this.geomSphereDirty = true;
    this.boundSpaceDirty = true;
    this.parentCoordinatesDirty = true;
    if (WbBoundingSphere.updatesEnabled)
      this.parentUpdateNotification();
  }

  set(center, radius) {
    if (this.center.equal(center) && this.radius === radius)
      return;
    mCenter = center;
    mRadius = radius;
    if (!gRayTracingEnabled) {
      mBoundSpaceDirty = true;
      mParentCoordinatesDirty = true;
      if (gUpdatesEnabled)
        parentUpdateNotification();
    }
  }
}
