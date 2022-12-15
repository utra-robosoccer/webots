import WbWrenRenderingContext from './WbWrenRenderingContext.js';
import WbWrenShaders from './WbWrenShaders.js';
import {arrayXPointerFloat, arrayXPointerInt} from '../nodes/utils/utils.js';

export default class WbCoordinateSystem {
  #axesMaterial;
  #axesMesh;
  #font;
  #labelsMaterial;
  #labelsMesh;
  #labelsTexture;
  #labelsTransform;
  #renderables;
  #transform;
  constructor() {
    const labelMeshCoords = [-0.5, -0.5, 0, -0.5, 0.5, 0, 0.5, -0.5, 0, 0.5, 0.5, 0];
    const labelMeshCoordsPointer = arrayXPointerFloat(labelMeshCoords);

    const labelMeshIndices = [2, 1, 0, 3, 1, 2];
    const labelMeshIndicesPointer = arrayXPointerInt(labelMeshIndices);

    const labelTexCoords = [0, 0, 0, 1, 1, 0, 1, 1];
    const labelTexCoordsPointer = arrayXPointerFloat(labelTexCoords);

    // Null normals as we wont be using them
    const labelMeshNormals = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
    const labelMeshNormalsPointer = arrayXPointerFloat(labelMeshNormals);

    // Labels
    this.#labelsMesh = _wr_static_mesh_new(4, 6, labelMeshCoordsPointer, labelMeshNormalsPointer, labelTexCoordsPointer,
      labelTexCoordsPointer, labelMeshIndicesPointer, false);

    _free(labelMeshCoordsPointer);
    _free(labelMeshIndicesPointer);
    _free(labelTexCoordsPointer);
    _free(labelMeshNormalsPointer);

    const labelsOffset = [[1.15, 0, 0], [0, 1.15, 0], [0, 0, 1.15]];

    this.#transform = _wr_transform_new();

    // this.#font = _wr_font_new();
    // TODO AIE
    // _wr_font_set_face(this.#font, 'arial');
    // _wr_font_set_size(this.#font, 64);

    const labelsColor = [[0, 0, 1, 1], [0, 1, 0, 1], [1, 0, 0, 1]];
    const labels = ['X', 'Y', 'Z'];
    const labelsScale = 0.3;

    // Setup coordinate system position & scale
    const globalScale = 0.1;
    const scale = _wrjs_array3(globalScale, globalScale, globalScale);
    _wr_transform_set_scale(this.#transform, scale);
    const position = _wrjs_array3(0, 0, -0.5);
    _wr_transform_set_position(this.#transform, position);

    const screenPosition = [0.9, -0.9];
    const screenPositionPointer = arrayXPointerFloat(screenPosition);
    const shader = WbWrenShaders.coordinateSystemShader();

    Module.ccall('wr_shader_program_set_custom_uniform_value', null, ['number', 'string', 'number', 'number'],
      [shader, 'screenPosition', Enum.WR_SHADER_PROGRAM_UNIFORM_TYPE_VEC2F, screenPositionPointer]);
    _free(screenPositionPointer);

    Module.ccall('wr_shader_program_set_custom_uniform_value', null, ['number', 'string', 'number', 'number'],
      [shader, 'size', Enum.WR_SHADER_PROGRAM_UNIFORM_TYPE_FLOAT, _wrjs_pointerOnFloat(globalScale)]);

    const axesCoordinates = [[0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 1]];

    const axesColor = [[1, 0, 0], [0, 1, 0], [0, 0, 1]];

    // Create axes & their labels
    this.#axesMaterial = [];
    this.#axesMesh = [];
    this.#renderables = [[], [], []];
    for (let i = 0; i < 3; ++i) {
      // Axis
      const axesCoordinatesIPointer = arrayXPointerFloat(axesCoordinates[i]);
      this.#axesMesh[i] = _wr_static_mesh_line_set_new(2, axesCoordinatesIPointer, undefined);
      _free(axesCoordinatesIPointer);
      this.#axesMaterial[i] = _wr_phong_material_new();

      const axesColorPointer = _wrjs_array3(axesColor[i][0], axesColor[i][1], axesColor[i][2]);
      _wr_phong_material_set_color(this.#axesMaterial[i], axesColorPointer);
      _wr_material_set_default_program(this.#axesMaterial[i], WbWrenShaders.coordinateSystemShader());

      let renderable = _wr_renderable_new();
      this.#renderables[i][0] = renderable;
      _wr_renderable_set_cast_shadows(renderable, false);
      _wr_renderable_set_receive_shadows(renderable, false);
      _wr_renderable_set_mesh(renderable, this.#axesMesh[i]);
      _wr_renderable_set_material(renderable, this.#axesMaterial[i], undefined);
      _wr_renderable_set_drawing_order(renderable, Enum.WR_RENDERABLE_DRAWING_ORDER_AFTER_2);
      _wr_renderable_set_drawing_mode(renderable, Enum.WR_RENDERABLE_DRAWING_MODE_LINES);
      _wr_renderable_set_visibility_flags(renderable, WbWrenRenderingContext.VF_INVISIBLE_FROM_CAMERA);
      _wr_renderable_set_scene_culling(renderable, false);
      _wr_renderable_set_in_view_space(renderable, true);
      _wr_renderable_set_z_sorted_rendering(renderable, true);

      _wr_transform_attach_child(this.#transform, renderable);

      // Label
      renderable = _wr_renderable_new();
      this.#renderables[i][1] = renderable;

      this.#labelsTexture[i] = _wr_drawable_texture_new();

      let width, height;
      // _wr_font_get_bounding_box(this.#font, labels[i], width, height);

      _wr_texture_set_size(this.#labelsTexture[i], width, height);
      _wr_texture_set_translucent(this.#labelsTexture[i], true);
      _wr_drawable_texture_set_use_premultiplied_alpha(this.#labelsTexture[i], true);
      _wr_drawable_texture_set_color(this.#labelsTexture[i], labelsColor[i]);
      _wr_drawable_texture_set_font(this.#labelsTexture[i], this.#font);
      _wr_texture_setup(this.#labelsTexture[i]);
      _wr_drawable_texture_clear(this.#labelsTexture[i]);
      _wr_drawable_texture_draw_text(this.#labelsTexture[i], labels[i], 0, 0);

      this.#labelsMaterial[i] = _wr_phong_material_new();
      _wr_material_set_default_program(this.#labelsMaterial[i], shader);
      _wr_material_set_texture(this.#labelsMaterial[i], this.#labelsTexture[i], 0);

      _wr_renderable_set_cast_shadows(renderable, false);
      _wr_renderable_set_receive_shadows(renderable, false);
      _wr_renderable_set_mesh(renderable, this.#labelsMesh);
      _wr_renderable_set_material(renderable, this.#labelsMaterial[i], undefined);
      _wr_renderable_set_drawing_order(renderable, Enum.WR_RENDERABLE_DRAWING_ORDER_AFTER_2);
      _wr_renderable_set_visibility_flags(renderable, WbWrenRenderingContext.VF_INVISIBLE_FROM_CAMERA);
      _wr_renderable_set_scene_culling(renderable, false);
      _wr_renderable_set_in_view_space(renderable, true);
      _wr_renderable_set_z_sorted_rendering(renderable, true);

      this.#labelsTransform[i] = _wr_transform_new();

      const labelsOffsetPointer = _wrjs_array3(labelsOffset[i][0], labelsOffset[i][1], labelsOffset[i][2]);
      _wr_transform_set_position(this.#labelsTransform[i], labelsOffsetPointer);
      const aspectRatio = width / height;
      const transformScale = [aspectRatio * labelsScale, labelsScale, 1];
      _wr_transform_set_scale(this.#labelsTransform[i], transformScale);

      _wr_transform_attach_child(this.#labelsTransform[i], renderable);
      _wr_transform_attach_child(this.#transform, this.#labelsTransform[i]);
    }

    const root = _wr_scene_get_root(_wr_scene_get_instance());
    _wr_transform_attach_child(root, this.#transform);
  }

  deleteWrenObjects() {
    _wr_node_delete(this.#transform);
    _wr_static_mesh_delete(this.#labelsMesh);
    // _wr_font_delete(this.#font);

    for (let i = 0; i < 3; ++i) {
      _wr_node_delete(this.#renderables[i][0]);
      _wr_node_delete(this.#renderables[i][1]);

      _wr_static_mesh_delete(this.#axesMesh[i]);

      _wr_material_delete(this.#axesMaterial[i]);
      _wr_material_delete(this.#labelsMaterial[i]);

      _wr_node_delete(this.#labelsTransform[i]);

      _wr_texture_delete(this.#labelsTexture[i]);
    }
  }
}
