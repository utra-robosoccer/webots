import WbVector3 from './WbVector3.js';

export default class WbRay {
  constructor(origin = new WbVector3(), direction = new WbVector3()) {
    this.origin = origin;
    this.direction = direction;
  }
}
