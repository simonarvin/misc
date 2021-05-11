import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
from pathlib import Path


frames_per_sec = 120 #default ISCAN framerate- samps/sec
min_spacing = 50

#Subtract_corneal_reflection
#cr = 0 by default
#OKR = xxx (absolut)
#ETMs = xxxx (ratio)
# :)
# se om du kan gemme filen som .fig, eller imageJ
# gem automatisk i folder som data

try:
    threshold = float(sys.argv[2])

except:
    print("add the second command line argument\nfor example:\npython OKR_counter.py path/to/file 20")
    sys.exit(0)

cr = False
if len(sys.argv) > 3:
    if sys.argv[3] == "0":
        cr = False
    else:
        cr = True

plt.style.use(plt.style.available[2])
class Counter:
    def __init__(self):
        try:
            self.filename = sys.argv[1]
        except IndexError:
            print("error: insert log file path as command line argument 1")
            sys.exit(0)
            return

        self.window_width = 10

        self.load_log()

    def mov_avg(self, data):
        cumsum_vec = np.cumsum(np.insert(data, 0, 0))
        return (cumsum_vec[self.window_width:] - cumsum_vec[:-self.window_width]) / self.window_width

    def load_log(self):
        print("loading log...")
        self.log = pd.read_csv(self.filename, delimiter="\t", skiprows = 28)



        print("log loaded!")
        y = self.log[["Pupil H1 "]][1:]
        y = y.to_numpy(dtype=np.float64).flatten()

        cr_y = self.log[["C.R. H1  "]][1:]

        cr_y = cr_y.to_numpy(dtype=np.float64).flatten()
        cr_y = cr_y[y != 0]

        y = y[y != 0]
        total_frames = y.shape[0]
        if cr:
            y -= cr_y

        y = self.mov_avg(y)

        x = np.arange(y.shape[0])
        fps = 120

        dy = frames_per_sec * np.diff(y) #gives pixels movement per second

        subtracted_frames = 0
        #x_mark = x.copy()
        bool_condition = np.abs(dy) > threshold
        remove_condition = np.zeros(y.shape[0], dtype=bool)

        if len(sys.argv) > 4:
            filter = sys.argv[4].split(",")

            if len(filter) % 2 != 0:
                filter.append(len(bool_condition) - 1)


            i = 0

            while i < len(filter):
                bool_condition[int(filter[i]):int(filter[i + 1])] = False
                remove_condition[int(filter[i]):int(filter[i + 1])] = True
                subtracted_frames += int(filter[i]) - int(filter[i + 1])
                i += 2


        start = -1
        for i, entry in enumerate(bool_condition):
            if entry:
                if start == -1:
                    start = i
                else:
                    if i - start < min_spacing:
                        bool_condition[i] = False
                    else:
                        start = i

        #print(x.shape, y.to_np(dtype=np.float64).flatten())

        plt.plot(x, y, color = "#808080", lw = 2)
        plt.plot(x[remove_condition], y[remove_condition], color = "#a30000", lw = 2)
        plt.scatter(x[1:][bool_condition], y[1:][bool_condition], marker = "o", color = "magenta", s=10, zorder=10)
        okrs = np.sum(bool_condition)
        frames_left = total_frames - subtracted_frames

        ETMs = okrs/(frames_left/120/60/10)

        output = f"""
        datafile: {self.filename}
        (!) Threshold: {threshold}
        (!) OKR: {okrs}
        (!) ETMs: {round(ETMs, 2)} (OKRs/10min)
        (!) CR subtraction: {cr}

        ------
        Total frames:
        {total_frames} frames ({round(total_frames/fps/60, 1)} min)

        Frames included:
        {frames_left} frames ({round(frames_left/fps/60, 1)} min)

        Frames excluded:
        {subtracted_frames} frames ({round(subtracted_frames/fps/60, 1)} min)
        """
        print(output)


        
        datafile = os.path.splitext(self.filename)[0]
        log_path = f"{datafile}.log"
        with open(log_path, "w") as file:
            file.write(output)

        print(f"log saved: {log_path}")
        fig_path = f"{datafile}.pdf"

        plt.savefig(fig_path)

        print(f"figure saved: {fig_path}")


        plt.show()


c = Counter()
