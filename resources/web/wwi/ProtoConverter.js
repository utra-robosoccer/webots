import Proto from './protoDesigner/classes/Proto.js';

import {getAnId} from '../wwi/nodes/utils/id_provider.js';

export default class protoConverter {
  constructor(view) {
    this._view = view;
    this.loadMinimalScene();
  }

  loadProto(url, parentId) {
    return new Promise((resolve, reject) => {
      const xmlhttp = new XMLHttpRequest();
      xmlhttp.open('GET', url, true);
      xmlhttp.overrideMimeType('plain/text');
      xmlhttp.onreadystatechange = async() => {
        if (xmlhttp.readyState === 4 && (xmlhttp.status === 200 || xmlhttp.status === 0)) // Some browsers return HTTP Status 0 when using non-http protocol (for file://)
          resolve(xmlhttp.responseText);
      };
      xmlhttp.send();
    }).then(text => {
      const proto = new Proto(text);
      proto.parseBody();

      setTimeout(() => this._view.x3dScene._loadObject(proto.x3d, parentId), 3000);
    });
  }

  loadMinimalScene() {
    const xml = document.implementation.createDocument('', '', null);
    const scene = xml.createElement('Scene');

    let worldinfo = xml.createElement('WorldInfo');
    worldinfo.setAttribute('id', getAnId());
    worldinfo.setAttribute('basicTimeStep', '32');

    let viewpoint = xml.createElement('Viewpoint');
    viewpoint.setAttribute('id', getAnId());
    viewpoint.setAttribute('position', '0 0 0.7686199');
    viewpoint.setAttribute('exposure', '1');
    viewpoint.setAttribute('bloomThreshold', '21');
    viewpoint.setAttribute('zNear', '0.05');
    viewpoint.setAttribute('zFar', '0');
    viewpoint.setAttribute('ambientOcclusionRadius', '2');

    let background = xml.createElement('Background');
    background.setAttribute('id', getAnId());
    background.setAttribute('skyColor', '0.15 0.45 1');

    scene.appendChild(worldinfo);
    scene.appendChild(viewpoint);
    scene.appendChild(background);
    xml.appendChild(scene);

    const x3d = new XMLSerializer().serializeToString(xml);
    this._view.open(x3d, 'x3d', '', true);
  }
}
