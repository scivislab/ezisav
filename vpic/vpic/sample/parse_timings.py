# total number of processors used
proc = 512

# lines to parse timing information from
parselines = []
parselines.append("Execute vtkPVTrivialProducer id: 321,  ")
parselines.append("Execute vtkPythonProgrammableFilter id:,  ")
parselines.append("Execute vtkThreshold id: 345,  ")
parselines.append("Execute vtkCompleteArrays id: 357,  ")
parselines.append("Execute vtkFileSeriesWriter id: 379,  ")
parselines.append("    Execute vtkXMLPUnstructuredGridWriter i,  ")

# used to keep track of highest timing information from processors
highesttimes = [0] * len(parselines)
highesttimesend = [0] * len(parselines)

# counters to keep track of loops
counter1 = 0
counter2 = 0

limit = 10000
limitcounter = 0

# main loop
with open("timing_log.txt") as f:
    for line in f:
        for parseline in parselines:
            if line.startswith(parseline):
                line = line[len(parseline):]
                line = line[:-8]
                num = float(line)
                if (num > highesttimes[counter1]):
                    highesttimes[counter1] = num
                counter1 += 1
                if counter1 == len(parselines):
                    counter1 = 0
                    counter2 += 1
                    if counter2 == proc:
                        limitcounter += 1
                        counter2 = 0
                        for i in range(0,len(parselines)):
                            highesttimesend[i] += highesttimes[i]
                        highesttimes = [0] * len(parselines)
        if (limitcounter > limit):
            break

# print out results
total = 0
print ""
print "RESULTS:"
for i in range(0,len(parselines)):
    total += highesttimesend[i]
    print parselines[i] + str(highesttimesend[i]) + " seconds"
print "Total time: " + str(total) + " seconds"
print ""
