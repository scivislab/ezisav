
from paraview.simple import *
from paraview import coprocessing
#from mpi4py import MPI
#--------------------------------------------------------------
# Code generated from cpstate.py to create the CoProcessor.
# ParaView 4.4.0 64 bits

outputfrequency = 20

print 'in contourbenchmark.py'

# ----------------------- CoProcessor definition -----------------------

def CreateCoProcessor():
  def _CreatePipeline(coprocessor, datadescription):
    class Pipeline:
      # state file generated using paraview version 4.4.0

      # ----------------------------------------------------------------
      # setup the data processing pipelines
      # ----------------------------------------------------------------

      #### disable automatic camera reset on 'Show'
      paraview.simple._DisableFirstRenderCameraReset()

      # create a new 'XML Partitioned Image Data Reader'
      # create a producer from a simulation input
      filename_ = coprocessor.CreateProducer(datadescription, 'input')

      # create a new 'Contour'
      contour1 = Contour(Input=filename_)
      contour1.ContourBy = ['POINTS', 'Charge Density(Hhydro)']
      contour1.ComputeScalars = 1
      contour1.Isosurfaces = [0.543697, 0.7281374285714286, 0.9125778571428571, 1.0970182857142856, 1.2814587142857141, 1.4658991428571428, 1.6503395714285714, 1.83478]
      contour1.PointMergeMethod = 'Uniform Binning'

      # create a new 'Parallel PolyData Writer'
      parallelPolyDataWriter1 = servermanager.writers.XMLPPolyDataWriter(Input=contour1)

      # register the writer with coprocessor
      # and provide it with information such as the filename to use,
      # how frequently to write the data, etc.
      coprocessor.RegisterWriter(parallelPolyDataWriter1, filename='contour_%t.pvtp', freq=outputfrequency)

    return Pipeline()

  class CoProcessor(coprocessing.CoProcessor):
    def CreatePipeline(self, datadescription):
      self.Pipeline = _CreatePipeline(self, datadescription)

  coprocessor = CoProcessor()
  # these are the frequencies at which the coprocessor updates.
  freqs = {'input': [outputfrequency]}
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

    from mpi4py import MPI
    if MPI.COMM_WORLD.Get_rank() == 0:
      print 'doing coprocessing at time step ', datadescription.GetTimeStep()

    # Update the coprocessor by providing it the newly generated simulation data.
    # If the pipeline hasn't been setup yet, this will setup the pipeline.
    coprocessor.UpdateProducers(datadescription)

    # Write output data, if appropriate.
    coprocessor.WriteData(datadescription);

    # Write image capture (Last arg: rescale lookup table), if appropriate.
    coprocessor.WriteImages(datadescription, rescale_lookuptable=False)

    # Live Visualization, if enabled.
    coprocessor.DoLiveVisualization(datadescription, "localhost", 22222)


def Finalize():
  #name = 'benchmark_'+str(MPI.COMM_WORLD.Get_rank())+'.log'
  #pvb.dump_logs(name) not currently working
  print 'in finalize'


