import math

def computeStep(rangeX, rangeY, N, v=2, sigma=0.95): #useSteps = 0
    num = rangeX*rangeY*v*sigma
    den = N*pow((1-sigma),0.5)
    step = pow(num/den,0.5)
    resultX = int(math.floor(rangeX / step))
    resultY = int(math.floor(rangeY / step))
    if(resultX<=2):
        resultX=2
    if(resultY<=2):
        resultY=2
    return [resultX,resultY]

def computeStepNormalized(N, v=2, sigma=0.95): #useSteps = 2
    return int(math.floor(1 / float(math.sqrt((v*sigma)/(N*math.sqrt(1-sigma))))))

def computeStepV2(rangeData, N, v=2, sigma=0.95): #useSteps = 2
    if(rangeData>(pow(N,0.5)/2)):
        num = rangeData*v*sigma
        den = N*pow((1-sigma),0.5)
        step = pow(num/den,0.5)
        result = int(math.floor(rangeData / step))
    else:
        result = rangeData
    return int(result)