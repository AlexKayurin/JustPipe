import numpy as np
from PySide6.QtCore import QPointF
import pyqtgraph as pg

app = pg.mkQApp()

# 1. Create the ImageView widget and some background imagery
imv = pg.ImageView()
imv.show()

# Dummy image data
img_data = np.zeros((100, 100, 50))
imv.setImage(img_data)

# Fetch the ViewBox from the ImageView
view_box = imv.getView()

# 2. Generate line data and create a PlotDataItem
x_data = np.linspace(10, 90, 50)
y_data = np.sin(x_data / 10) * 20 + 50
plot_item = pg.PlotDataItem(x_data, y_data, pen=pg.mkPen('g', width=3))

# 3. Create a graphics group, add the plot to it, and rotate it
group = pg.ItemGroup()
view_box.addItem(group)  # Add group directly to the view layout
group.addItem(plot_item)  # Nest the plot item inside the group

# Apply transformations (e.g., rotate by -25 degrees around point 50,50)
group.setTransformOriginPoint(50, 50)
group.setRotation(-25)


# 4. Define the mouse callback function
def mouse_moved(evt):
  pos = evt  # Scene coordinate (QPointF)

  if view_box.sceneBoundingRect().contains(pos):
    # CRITICAL STEP: Map directly from Scene to the PlotDataItem's local space
    local_pos = plot_item.mapFromScene(pos)

    # These match your original x_data and y_data coordinate spaces!
    world_x, world_y = local_pos.x(), local_pos.y()

    print(f'True World Plot Data -> X: {world_x:6.2f} | Y: {world_y:6.2f}')


# 5. Connect the signal
imv.scene.sigMouseMoved.connect(mouse_moved)

if __name__ == '__main__':
  pg.exec()
