import numpy as np
import matplotlib.pyplot as plt

# Create a 3D sphere
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)

x = np.outer(np.cos(u), np.sin(v))
y = np.outer(np.sin(u), np.sin(v))
z = np.outer(np.ones_like(u), np.cos(v))

# Surface normals of the sphere
normals = np.stack((x, y, z), axis=-1)

# Normalize surface normals
normals = normals / np.linalg.norm(normals, axis=-1, keepdims=True)

# Light source position
light = np.array([2, 2, 3], dtype=float)
light = light / np.linalg.norm(light)

# Viewer position
view = np.array([0, 0, 1], dtype=float)

# Normalize view vector
view = view / np.linalg.norm(view)

# Material and lighting coefficients
ka = 0.2       # Ambient coefficient
kd = 0.6       # Diffuse coefficient
ks = 0.8       # Specular coefficient
shininess = 30 # Shininess exponent

# Ambient illumination
ambient = ka

# Diffuse illumination
diffuse = kd * np.maximum(np.sum(normals * light, axis=-1), 0)

# Reflection vector
dot_nl = np.sum(normals * light, axis=-1, keepdims=True)
reflection = 2 * dot_nl * normals - light

# Specular illumination
dot_rv = np.sum(reflection * view, axis=-1)
specular = ks * np.maximum(dot_rv, 0) ** shininess

# Total illumination
intensity = ambient + diffuse + specular

# Limit intensity to valid range
intensity = np.clip(intensity, 0, 1)

# Create RGB colors
colors = np.zeros((*x.shape, 4))
colors[..., 0] = intensity       # Red
colors[..., 1] = intensity * 0.5 # Green
colors[..., 2] = intensity * 0.2 # Blue
colors[..., 3] = 1                # Alpha

# Display the 3D sphere
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

ax.plot_surface(
    x, y, z,
    facecolors=colors,
    linewidth=0,
    antialiased=True,
    shade=False
)

ax.set_title("Phong Illumination Model")
ax.set_xlabel("X-axis")
ax.set_ylabel("Y-axis")
ax.set_zlabel("Z-axis")

ax.set_box_aspect([1, 1, 1])
plt.show()