import wdsflib

wdsf = wdsflib.WDSFFile('standardfile.wdsf')
wdsf_testing_data = wdsf.read(args=[['x', 10], ['y', 20]])
print(wdsf_testing_data)
wdsflib.convert_to_wdsf(wdsf_testing_data, 'output.wdsf')