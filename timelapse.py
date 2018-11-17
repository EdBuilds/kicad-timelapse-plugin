import pcbnew
import os
import re
import shutil
from timer import RepeatedTimer
from svg_processor import SvgProcessor
import sched, time

capture_interval=10

layers = [
    {
        'layer': pcbnew.B_SilkS,
        'name' :'B_SilkS',
        'color': '#CC00CC',
        'alpha': 0.8,
    },
    {
        'layer': pcbnew.B_Cu,
        'name' : 'B_Cu',
        'color': '#33EE33',
        'alpha': 0.5,
    },
    {
        'layer': pcbnew.F_Cu,
        'name' : 'F_Cu',
        'color': '#CC0000',
        'alpha': 0.5,
    },
    {
        'layer': pcbnew.F_SilkS,
        'name' : 'F_SilkS',
        'color': '#00CCCC',
        'alpha': 0.8,
    },
    {
        'layer': pcbnew.Cmts_User,
        'name' : 'Cmts_User',
        'color': '#333333',
        'alpha': 0.8,
    },
    {
        'layer': pcbnew.Edge_Cuts,
        'name' : 'Edge_Cuts',
        'color': '#3333CC',
        'alpha': 0.8,
    },
]


def extract_biggest_number(files):
    numbers=[]
    regex = re.compile(r'\d+')
    for sFile in files:
        print("found file:"+sFile)
        extracted_nums=regex.findall(sFile)
        if extracted_nums:
            print("Recognised num:"+str(extracted_nums))
            numbers.append(extracted_nums[0])
    return int(max(numbers)) if numbers else 0


class SimplePlugin(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "Timelapse recorder"
        self.category = "A descriptive category name"
        self.description = "A description of the plugin and what it does"

    def screenshot(self):
        print("Taking a screenshot")
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

        timelapse_files=os.listdir(timelapse_folder_path)
        timelapse_number=extract_biggest_number(timelapse_files)
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

        # Plot single layer to file

        timelapse_number += 1
        processed_svg_files = []
        for layer in layers:
            pc.SetLayer(layer['layer'])
            layer['layer']
            pc.OpenPlotfile('-'+layer['name']+'-'+str(timelapse_number).zfill(4), pcbnew.PLOT_FORMAT_SVG, layer['name'])
            pc.PlotLayer()
            pc.ClosePlot()
            output_filename = pc.GetPlotFileName()
            processor = SvgProcessor(output_filename)
            def colorize(original):
                if original.lower() == '#000000':
                    return layer['color']
                return original
            processor.apply_color_transform(colorize)
            processor.wrap_with_group({
                'opacity': str(layer['alpha']),
            })

            output_filename2 = os.path.join(timelapse_folder_path, 'processed-' + os.path.basename(output_filename))
            processor.write(output_filename2)
            processed_svg_files.append((output_filename2, processor))
            os.remove(output_filename)

        final_svg = os.path.join(timelapse_folder_path, board_filename_noex+'-'+str(timelapse_number).zfill(4)+'.svg')
        shutil.copyfile(processed_svg_files[0][0], final_svg)
        output_processor = SvgProcessor(final_svg)
        for processed_svg_file, processor in processed_svg_files:
            output_processor.import_groups(processor)
            os.remove(processed_svg_file)
        output_processor.write(final_svg)


    def Run(self):
        rt = RepeatedTimer(1, self.screenshot)


SimplePlugin().register() # Instantiate and register to Pcbnew
