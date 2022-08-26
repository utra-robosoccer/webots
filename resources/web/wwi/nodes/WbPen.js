import WbSolid from './WbSolid.js';

export default class WbPen extends WbSolid {
  constructor(id, translation, scale, rotation, inkColor, inkDensity, leadSize, write, maxDistance) {
    super(id, translation, scale, rotation);
    this.inkColor = inkColor;
    this.inkDensity = inkDensity;
    this.leadSize = leadSize;
    this.write = write;
    this.maxDistance = maxDistance;
  }
}
