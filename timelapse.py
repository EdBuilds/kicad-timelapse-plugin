import pcbnew
import os

layers = [
    {
        'layer': pcbnew.B_SilkS,
        'color': '#CC00CC',
        'alpha': 0.8,
    },
    {
        'layer': pcbnew.B_Cu,
        'color': '#33EE33',
        'alpha': 0.5,
    },
    {
        'layer': pcbnew.F_Cu,
        'color': '#CC0000',
        'alpha': 0.5,
    },
    {
        'layer': pcbnew.F_SilkS,
        'color': '#00CCCC',
        'alpha': 0.8,
    },
    {
        'layer': pcbnew.Cmts_User,
        'color': '#333333',
        'alpha': 0.8,
    },
    {
        'layer': pcbnew.Edge_Cuts,
        'color': '#3333CC',
        'alpha': 0.8,
    },
]
class SimplePlugin(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "Timelapse recorder"
        self.category = "A descriptive category name"
        self.description = "A description of the plugin and what it does"

    def Run(self):
        board = pcbnew.GetBoard()
        board_path=board.GetFileName()
        board_filename=os.path.basename(board_path)
        board_filename_noex=os.path.splitext(board_filename)[0]
        project_folder=os.path.dirname(board_path)
        timelapse_folder=board_filename_noex+'-timelapse'
        timelapse_folder_path=os.path.join(project_folder, timelapse_folder)
        if not os.path.exists(timelapse_folder_path):
            print('Timelapse folder does not exist. creating one now')
            os.mkdir(timelapse_folder_path)
            print('Timelapse folder created')

        pc = pcbnew.PLOT_CONTROLLER(board)
        po = pc.GetPlotOptions()
        po.SetOutputDirectory(timelapse_folder_path)
        po.SetPlotFrameRef(False)
        po.SetLineWidth(pcbnew.FromMM(0.35))
        po.SetScale(1)
        po.SetUseAuxOrigin(True)
        po.SetMirror(False)
        po.SetExcludeEdgeLayer(True)
        # Set current layer
        pc.SetLayer(pcbnew.F_Cu)

        # Plot single layer to file
        pc.OpenPlotfile("front_copper", pcbnew.PLOT_FORMAT_SVG, "front_copper")
        print("Plotting to " + pc.GetPlotFileName())
        pc.PlotLayer()
        pc.ClosePlot()


SimplePlugin().register() # Instantiate and register to Pcbnew
