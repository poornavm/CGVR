Shader "Lab8/VertexFragment"
{
    SubShader
    {
        Tags { "RenderType"="Opaque" }
        Pass
        {
            Cull Off
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #include "UnityCG.cginc"
            float4x4 _Transform2D;
            struct Input { float4 vertex : POSITION; float4 color : COLOR; };
            struct Output { float4 position : SV_POSITION; float4 color : COLOR; };
            Output vert(Input v)
            {
                Output o;
                // Homogeneous model transformation, followed by view and projection.
                o.position = UnityObjectToClipPos(mul(_Transform2D, v.vertex));
                o.color = v.color;
                return o;
            }
            fixed4 frag(Output i) : SV_Target { return i.color; }
            ENDCG
        }
    }
}
