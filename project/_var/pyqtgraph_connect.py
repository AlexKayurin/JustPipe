import numpy as np
import pyqtgraph as pg

app = pg.mkQApp()
win = pg.GraphicsLayoutWidget()
plot = win.addPlot()

# 1. Define 5 data points
x = np.array([0, 1, 2, 3, 4])
y = np.array([1, 3, 2, 4, 3])

# 2. Define connectivity mask (Size N or N-1)
# True = draw line to next point, False = break line
# Connects: 0->1 (True), 1->2 (False), 2->3 (True), 3->4 (False)
connect_mask = np.array([1, 0, 1, 0, 0], dtype=np.int32)

# 3. Plot using the mask array
curve = pg.PlotDataItem(x, y, connect=connect_mask, pen=pg.mkPen('cyan', width=2))
plot.addItem(curve)

win.show()
app.exec()