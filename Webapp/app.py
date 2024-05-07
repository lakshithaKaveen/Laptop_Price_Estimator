from flask import Flask, render_template, request
import pickle
import numpy as np

# setup application
app = Flask(__name__)

def estimate(lst):
    filename = '../Model/priceEstimate.pickle'
    with open(filename, 'rb') as file:
        model = pickle.load(file)
    estimatedValue = model.predict([lst])
    return estimatedValue

@app.route('/', methods=['POST', 'GET'])
def index():
    estimatedValue = 0
    if request.method == 'POST':
        ram = request.form['ram']
        weight = request.form['weight']
        company = request.form['company']
        typename = request.form['typename']
        opsys = request.form['opsys']
        cpu = request.form['cpuname']
        gpu = request.form['gpuname']
        touchscreen = request.form.getlist('touchscreen')
        ips = request.form.getlist('ips')
        
        featureList = []

        featureList.append(int(ram))
        featureList.append(float(weight))
        featureList.append(len(touchscreen))
        featureList.append(len(ips))

        companyList = ['acer','apple','asus','dell','hp','lenovo','msi','other','toshiba']
        typenameList = ['2in1convertible','gaming','netbook','notebook','ultrabook','workstation']
        opSysList = ['linux','mac','other','windows']
        CPUList = ['amd','intelcorei3','intelcorei5','intelcorei7','other']
        GPUList = ['amd','intel','nvidia']

        def traverse_list(lst, value):
            for item in lst:
                if item == value:
                    featureList.append(1)
                else:
                    featureList.append(0)
        
        traverse_list(companyList, company)
        traverse_list(typenameList, typename)
        traverse_list(opSysList, opsys)
        traverse_list(CPUList, cpu)
        traverse_list(GPUList, gpu)

        estimatedValue = estimate(featureList)
        estimatedValue = np.round(estimatedValue[0],2)*322

    return render_template('index.html', estimatedValue=estimatedValue)


if __name__ == '__main__':
    app.run(debug=True)