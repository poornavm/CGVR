using System.IO;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;

[InitializeOnLoad]
public static class LabSceneAutoSetup_lab8
{
    const string ScenePath = "Assets/Scenes/Lab8_VertexFragmentShaders.unity";
    static LabSceneAutoSetup_lab8() { EditorApplication.delayCall += CreateIfMissing; }
    static void CreateIfMissing()
    {
        if (Application.isPlaying || AssetDatabase.LoadAssetAtPath<SceneAsset>(ScenePath) != null) return;
        // Avoid replacing an unsaved scene the user is already editing.
        if (UnityEngine.SceneManagement.SceneManager.GetActiveScene().isDirty) return;
        Build();
    }
    [MenuItem("Lab 8/Create or Open Shader Scene")]
    static void Open()
    {
        if (!EditorSceneManager.SaveCurrentModifiedScenesIfUserWantsTo()) return;
        if (AssetDatabase.LoadAssetAtPath<SceneAsset>(ScenePath) != null)
            EditorSceneManager.OpenScene(ScenePath);
        else Build();
    }
    static void Build()
    {
        Shader shader = Shader.Find("Lab8/VertexFragment");
        if (shader == null) { Debug.LogError("Lab8 shader missing. Fix shader import errors first."); return; }
        Directory.CreateDirectory("Assets/Scenes");
        Directory.CreateDirectory("Assets/GeneratedMaterials");
        Directory.CreateDirectory("Assets/GeneratedMeshes");
        AssetDatabase.Refresh();
        var scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
        const string meshPath = "Assets/GeneratedMeshes/ColourTriangle.asset";
        Mesh mesh = AssetDatabase.LoadAssetAtPath<Mesh>(meshPath);
        if (mesh == null)
        {
            mesh = new Mesh { name = "ColourTriangle" };
            mesh.vertices = new[] { new Vector3(-1,-.8f,0), new Vector3(1,-.8f,0), new Vector3(0,1,0) };
            mesh.colors = new[] { Color.red, Color.green, Color.blue };
            mesh.triangles = new[] { 0, 1, 2 };
            // Vertex shader transformations must not be culled using the original bounds.
            mesh.bounds = new Bounds(Vector3.zero, Vector3.one * 10000);
            AssetDatabase.CreateAsset(mesh, meshPath);
        }
        const string matPath = "Assets/GeneratedMaterials/ShaderMaterial.mat";
        Material mat = AssetDatabase.LoadAssetAtPath<Material>(matPath);
        if (mat == null) { mat = new Material(shader); AssetDatabase.CreateAsset(mat, matPath); }
        mat.SetMatrix("_Transform2D", Matrix4x4.identity);
        var triangle = new GameObject("Shader Triangle");
        triangle.AddComponent<MeshFilter>().sharedMesh = mesh;
        triangle.AddComponent<MeshRenderer>().sharedMaterial = mat;
        triangle.AddComponent<ShaderDemo_lab8>();
        var cameraObj = new GameObject("Main Camera");
        cameraObj.tag = "MainCamera";
        var camera = cameraObj.AddComponent<Camera>();
        camera.orthographic = true; camera.orthographicSize = 3;
        camera.clearFlags = CameraClearFlags.SolidColor;
        camera.backgroundColor = new Color(.035f,.05f,.09f);
        cameraObj.transform.position = new Vector3(0,0,-10);
        EditorSceneManager.SaveScene(scene, ScenePath);
        EditorBuildSettings.scenes = new[] { new EditorBuildSettingsScene(ScenePath,true) };
        AssetDatabase.SaveAssets();
        Selection.activeGameObject = triangle;
    }
}
