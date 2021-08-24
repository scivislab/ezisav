
from paraview.simple import *
from paraview import coprocessing

import paraview
from paraview.vtk import vtkTimerLog
import benchmark
import sys

#--------------------------------------------------------------
# Code generated from cpstate.py to create the CoProcessor.
# ParaView 5.1.0 64 bits


# ----------------------- CoProcessor definition -----------------------

def CreateCoProcessor():
  def _CreatePipeline(coprocessor, datadescription):
    class Pipeline:
      # state file generated using paraview version 5.1.0

      # ----------------------------------------------------------------
      # setup the data processing pipelines
      # ----------------------------------------------------------------

      #### disable automatic camera reset on 'Show'
      paraview.simple._DisableFirstRenderCameraReset()

      # create a new 'XML Partitioned Polydata Reader'
      # create a producer from a simulation input
      contour_40pvtp = coprocessor.CreateProducer(datadescription, 'input')

      # create a new 'Programmable Filter'
      currentDensity = ProgrammableFilter(Input=contour_40pvtp)
      currentDensity.Script = 'import numpy\nimport paraview.numpy_support as ns\n\n# Get input and set output\ninput = self.GetInputDataObject(0, 0)\noutput = self.GetOutputDataObject(0)\n\noutput.ShallowCopy(input)\narray1 = input.GetPointData().GetArray("Current Density(ehydro)")\narray2 = input.GetPointData().GetArray("Current Density(Hhydro)")\n\n# Convert arrays to numpy arrays\narray1 = ns.vtk_to_numpy(array1)\narray2 = ns.vtk_to_numpy(array2)\n\nJ_X = array2[::1,0:1:1] + array1[::1,0:1:1]\nJ_Y = array2[::1,1:2:1] + array1[::1,1:2:1]\nJ_Z = array2[::1,2:3:1] + array1[::1,2:3:1]\n\nJ = numpy.sqrt(numpy.square(J_X)+numpy.square(J_Y)+numpy.square(J_Z))\n\nresult1 = ns.numpy_to_vtk(J, deep=1)\n\nresult1.SetName("J")\n\noutput.GetPointData().AddArray(result1)'
      currentDensity.RequestInformationScript = ''
      currentDensity.RequestUpdateExtentScript = ''
      currentDensity.PythonPath = ''

      # create a new 'Threshold'
      threshold1 = Threshold(Input=currentDensity)
      threshold1.Scalars = ['POINTS', 'J']
      threshold1.ThresholdRange = [0.1, 10.0]

      # create a new 'Parallel UnstructuredGrid Writer'
      parallelUnstructuredGridWriter1 = servermanager.writers.XMLPUnstructuredGridWriter(Input=threshold1)

      # register the writer with coprocessor
      # and provide it with information such as the filename to use,
      # how frequently to write the data, etc.
      coprocessor.RegisterWriter(parallelUnstructuredGridWriter1, filename='output_%t.pvtu', freq=20)

      # ----------------------------------------------------------------
      # finally, restore active source
      SetActiveSource(parallelUnstructuredGridWriter1)
      # ----------------------------------------------------------------
    return Pipeline()

  class CoProcessor(coprocessing.CoProcessor):
    def CreatePipeline(self, datadescription):
      self.Pipeline = _CreatePipeline(self, datadescription)

  coprocessor = CoProcessor()
  # these are the frequencies at which the coprocessor updates.
  freqs = {'input': [20]}
  coprocessor.SetUpdateFrequencies(freqs)
  return coprocessor

#--------------------------------------------------------------
# Global variables that will hold the pipeline for each timestep
# Creating the CoProcessor object, doesn't actually create the ParaView pipeline.
# It will be automatically setup when coprocessor.UpdateProducers() is called the
# first time.
coprocessor = CreateCoProcessor()

#--------------------------------------------------------------
# Enable Live-Visualizaton with ParaView
coprocessor.EnableLiveVisualization(True, 1)


# ---------------------- Data Selection method ----------------------

def RequestDataDescription(datadescription):
    "Callback to populate the request for current timestep"
    global coprocessor
    if datadescription.GetForceOutput() == True:
        # We are just going to request all fields and meshes from the simulation
        # code/adaptor.
        for i in range(datadescription.GetNumberOfInputDescriptions()):
            datadescription.GetInputDescription(i).AllFieldsOn()
            datadescription.GetInputDescription(i).GenerateMeshOn()
        return

    # setup requests for all inputs based on the requirements of the
    # pipeline.
    coprocessor.LoadRequestedData(datadescription)

# ------------------------ Processing method ------------------------

def DoCoProcessing(datadescription):
    "Callback to do co-processing for current timestep"
    global coprocessor

    # Update the coprocessor by providing it the newly generated simulation data.
    # If the pipeline hasn't been setup yet, this will setup the pipeline.
    coprocessor.UpdateProducers(datadescription)

    # Write output data, if appropriate.
    coprocessor.WriteData(datadescription);

    # Write image capture (Last arg: rescale lookup table), if appropriate.
    coprocessor.WriteImages(datadescription, rescale_lookuptable=False)

    # Live Visualization, if enabled.
    coprocessor.DoLiveVisualization(datadescription, "localhost", 22222)

    benchmark.get_logs()
    saveout = sys.stdout
    sys.stdout = open('timing_log.txt', 'a')
    benchmark.print_logs()
    sys.stdout = saveout
    vtkTimerLog.ResetLog()

