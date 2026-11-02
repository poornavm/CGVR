using UnityEngine;

// All deformation happens in the vertex shader; CPU builds homogeneous matrices.
public class ShaderDemo_lab8 : MonoBehaviour
{
    Material material;
    Vector2 translation;
    float angle, scale = 1f, shear;
    bool reflected;
    void Start()
    {
        material = GetComponent<MeshRenderer>().material;
        Apply();
    }
    void Update()
    {
        float dt = Time.deltaTime;
        if (Input.GetKey(KeyCode.LeftArrow)) translation.x -= dt;
        if (Input.GetKey(KeyCode.RightArrow)) translation.x += dt;
        if (Input.GetKey(KeyCode.UpArrow)) translation.y += dt;
        if (Input.GetKey(KeyCode.DownArrow)) translation.y -= dt;
        if (Input.GetKey(KeyCode.Q)) angle += 70f * dt;
        if (Input.GetKey(KeyCode.E)) angle -= 70f * dt;
        if (Input.GetKey(KeyCode.Z)) scale = Mathf.Max(.1f, scale - dt);
        if (Input.GetKey(KeyCode.X)) scale = Mathf.Min(3f, scale + dt);
        if (Input.GetKey(KeyCode.A)) shear -= dt;
        if (Input.GetKey(KeyCode.D)) shear += dt;
        shear = Mathf.Clamp(shear, -2f, 2f);
        if (Input.GetKeyDown(KeyCode.F)) reflected = !reflected;
        if (Input.GetKeyDown(KeyCode.R))
        { translation = Vector2.zero; angle = shear = 0; scale = 1; reflected = false; }
        Apply();
    }
    void Apply()
    {
        Matrix4x4 h = Matrix4x4.identity;
        h.m01 = shear;
        Matrix4x4 s = Matrix4x4.Scale(new Vector3(reflected ? -scale : scale, scale, 1));
        Matrix4x4 r = Matrix4x4.Rotate(Quaternion.Euler(0, 0, angle));
        Matrix4x4 t = Matrix4x4.Translate(new Vector3(translation.x, translation.y, 0));
        material.SetMatrix("_Transform2D", t * r * h * s);
    }
    void OnGUI()
    {
        GUI.Box(new Rect(12, 12, 620, 155), "EXPERIMENT 8 - VERTEX AND FRAGMENT SHADERS");
        GUI.Label(new Rect(25, 42, 590, 110),
            "Arrows: translate | Q/E: rotate | Z/X: scale\n" +
            "A/D: shear | F: reflect across Y-axis | R: reset\n" +
            "Matrix order: T * R * H * S (right to left)\n" +
            "Vertex shader: transforms positions. Fragment shader: interpolated colour.");
    }
    void OnDestroy() { if (material != null) Destroy(material); }
}
