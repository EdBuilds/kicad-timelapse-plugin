import pcbnew

class SimplePlugin(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "Timelapse recorder"
        self.category = "A descriptive category name"
        self.description = "A description of the plugin and what it does"

    def Run(self):
        # The entry function of the plugin that is executed on user action
        print("Hello World")
        x = pcbnew.FromMM(10)
        y = pcbnew.FromMM(10)
        width  = pcbnew.FromMM(20)
        height = pcbnew.FromMM(20)
        pcbnew.WindowZoom(5, 5, 5, 5)
        #:pcbnew.Refresh()

SimplePlugin().register() # Instantiate and register to Pcbnew
