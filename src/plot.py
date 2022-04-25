from matplotlib import pyplot as plt
import matplotlib.animation as animation
from matplotlib.ticker import MaxNLocator
import numpy as np

def plot_field(mesh,field,ncol,field_name,ID):

    # Helpful info: mesh  = meshObj
    #               field = p x 1 (ncol = 0) or p x t(specific ncol)
    #               field_name = string to name the saved im
    #               ID = another code to name the saved im

    aux      = np.zeros([mesh.nElements ,1])
    axField = np.zeros([mesh.nElementsD, mesh.nElementsL])

    for e in range(0 ,mesh.nElements):
        counter = 0
        for node in range(0, 4):
            counter += 0.25*field[mesh.Connect[e, node] - 1, ncol]
        aux[e ,0] = counter

    for j in range(0, mesh.nElementsD):
        for i in range(0, mesh.nElementsL):
            axField[(mesh.nElementsD - 1) - j, i] = aux[i + j * mesh.nElementsL, 0]

    fig1, ax = plt.subplots(figsize=(7, 7))
    ax.imshow(axField, cmap = 'binary')
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    plt.xlabel(' ')
    plt.ylabel(' ')
    plt.title(' ')
    plt.savefig(f'../../FWI_Python/plots/{field_name}_{ID}.png')
    plt.close(fig1)


def plot_cost(cF,it,niter):

    x = np.linspace(1, len(cF), len(cF), dtype=int)
    y = np.zeros([len(cF), 1])
    for i in range(0, len(cF)):
        y[i,0] = cF[i]
    fig1 = plt.figure(figsize=(7, 7))
    ax = fig1.gca()
    plt.plot(x, y, color='b', marker='o', label=' ')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.draw()
    plt.grid(True)
    plt.xlabel(' ')
    plt.ylabel(' ')
    plt.title(' ')
    if it >= niter - 2:
        plt.savefig('../../FWI_Python/plots/costFunctional.png')
    plt.show(block=False)
    plt.pause(.3)

    return fig1


def render_propagating(mesh,field,size):

    #Helpful info: mesh  = meshObj
    #              field = p x t
    #              size  = size of dt analysed

    ims = []
    steps = field.shape[1]//size

    aux = np.zeros([mesh.nElements, 1])
    axField = np.zeros([mesh.nElementsD, mesh.nElementsL])

    fig1, ax = plt.subplots(figsize=(7, 7))

    for t in range(0, steps):
        time = size * t
        if time < field.shape[1]:
            for e in range(0, mesh.nElements):
                counter = 0
                for node in range(0, 4):
                    counter += 0.25 * field[mesh.Connect[e, node] - 1, time]
                aux[e, 0] = counter

            for j in range(0, mesh.nElementsD):
                for i in range(0, mesh.nElementsL):
                    axField[(mesh.nElementsD - 1) - j, i] = aux[i + j * mesh.nElementsL, 0]

            im = ax.imshow(axField, cmap='binary', animated=True)
            ims.append([im])

    ani = animation.ArtistAnimation(fig1,ims,interval=5,blit=True,repeat_delay=800)

    plt.show()
