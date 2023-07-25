## 파트 1: 뉴런 및 간단한 신경 네트워크
- 원문: <a href="https://nest-simulator.readthedocs.io/en/stable/tutorials/pynest_tutorial/part_1_neurons_and_simple_neural_networks.html#pynest-tutorial-1">링크</a>
  - 안 중요한 내용은 적당히 뺐으니 정확한 내용은 반드시 원문을 참조

### 서론

### PyNEST - NEST 시뮬레이터 인터페이스

<img src ="https://nest-simulator.readthedocs.io/en/stable/_images/python_interface.png">

**Figure 1** 파이썬 인터페이스가 작동하는 방식. 파이썬 인터프리터가 nest 모듈을 인식하고 import하면, NEST Simulator kernel가 동적으로 로드된다. 사용자의 sim1ulation script에 쓰이는 function은 모두 이 high-level API에 정의되어 있으며 (즉, Python level), 이 함수들이 NEST의 기본 언어(시뮬레이션 언어)로 된 SLI code를 생성한 후 NEST simulation kernel을 제어한다.

NEural Simulation Tool (www.nest-initiative.org)은 대규모 이형 뉴런 네트워크를 시뮬레이션 하기 위해 설계된 GPL 라이선스 오픈 소스 소프트웨어이다. 시뮬레이터는 Python에 대한 interface를 제공한다. Figure 1은 사용자의 simulation script와 NEST Simulator 간의 상호작용을 묘사하고 있다. 높은 시뮬레이션 성능을 위해, 시뮬레이션 커널은 C++로 작성되었다.

파이썬에서 NEST API를 사용하고자 할 땐 import nest를 입력하면 된다. scikit-lean이나 scipy처럼 다른 package가 필요할 땐, 반드시 nest를 import하기 전에 import한다. dir(nest)를 입력하면 사용할 수 있는 함수(커맨드)들의 목록을 볼 수 있다. plot 기능을 사용하기 위해서는 Matplotlib를 import한다 (import matplotlib.pyplot as plt). 해당 라이브러리를 사용하면 결과를 display 또는 저장할 수 있다.


### 노드 만들기

- 모든 새 노드는 Create()함수로 만들 수 있다. 이 함수는 model(string), n(모델 개수. int, *optional*), params(dict or list, *optional*), positions(grid or free object, *optional*)를 인자로 받는다. <a href ="https://nest-simulator.readthedocs.io/en/stable/ref_material/pynest_apis.html#nest.lib.hl_api_nodes.Create">참조.</a> 함수의 반환값은 NodeCollection 오브젝트로, 정수값인 id로 대표된다. 대부분의 PyNEST 함수는 NodeCollection 오브젝트를 입력인자로 받거나 반환한다.

  - 사용할 수 있는 뉴런 노드의 타입(즉, model 부분에 들어갈 string 타입의 이름)에는 다음과 같은 종류가 있다.
    - "iaf_psc_alpha": alpha-shaped postsynaptic current를 가진 integrate-and-fire 모델. [파라미터 참조](https://nest-simulator.readthedocs.io/en/v3.3/models/iaf_psc_alpha_ps.html)
    - "hh_psc_alpha": [파라미터 참조](https://nest-simulator.readthedocs.io/en/v3.5/models/hh_psc_alpha.html)
    - "ht_neuron": [파라미터 참조](https://nest-simulator.readthedocs.io/en/v3.5/models/ht_neuron.html)
    - 등등...
    - [더 많은 모델 종류는 이 링크 참조](https://nest-simulator.readthedocs.io/en/v3.5/models/)

  - 이를테면 neuron = nest.Create("iaf_pcs_alpha")는 새 IF모델 뉴런 하나를 만드는 코드이다. 이렇게 형성한 오브젝트는 get() 메서드를 사용해 각종 파라미터의 값을 확인할 수 있다. get()의 인자는 하나일 수도 있고 (string 타입. 이 경우 반환값은 floating point element이다.), 여러 개를 한꺼번에 참조할 수도 있다 (string list 타입. 이 경우 반환값은 입력 인자의 요소들에 각기 대응되는 dictionary이다.)

  - 반대로, set() 메서드를 사용하면 만들어진 오브젝터의 파라미터를 직접 수정할 수 있다. 예를 들면, neuron.set(I_e = 500.0) 또는 neuron.set({"I_e": 500.0})과 같은 형식으로 입력하면 된다. dictionary 타입을 이용하여 인자를 넣으면 여러 개의 파라미터를 한꺼번에 입력할 수 있다. 이 때 주의할 점은, **NEST는 type sensitive**하기 때문에 double type으로 정의된 값들은 반드시 타입에 맞춰서 넣어주어야 한다! (이를테면 500은 파이썬 인터프리터에서 정수로 인식되기 때문에, NEST 인터프리터에서 타입 오류를 유발한다.)

  - 또한, 모델 오브젝트의 attribute에 값을 대입하는 방식으로도 파라미터의 값을 바꿀 수 있다. 예를 들면 neuron.I_e = 500.0을 입력해 I_e 파라미터를 직접 수정할 수 있다.

- 막전위 등 시간에 따라 변화하는 모델의 시뮬레이션 결과를 기록하기 위한 device 또한 오브젝트의 형태로 정의해야 한다. 이를 multemeter라고 하며, multemeter 노드 역시 Create()함수로 만들 수 있다. multemeter = nest.Create("multimeter")와 같이 모델 이름을 multimeter로 입력하면 되며, 이 모델의 record_from 파라미터는 측정하고 싶은 변수의 이름(string) 또는 이름 목록 (string list)를 인자로 받는다. (예: multimeter.set(record_from=["V_m"]))

- 한편, spike를 기록하기 위한 device 또한 모델로 정의할 수 있다. spikerecorder = nest.Create("spike_recorder")와 같이 사용하면 된다.


### 기본 연결로 노드 연결하기

- 위에서 생성한 노드들은 서로 연결을 해야만 상호작용을 하며 결과를 기록하고 시뮬레이션을 진행할 수 있다. nest.Conenct(n1, n2)는 두 노드 n1, n2를 서로 연결시켜주는 함수이다. 이를테면, 위에서 생성한 neuron의 시간에 따른 반응을 multimeter 및 spikerecorder로 측정하고 싶다면 nest.Connect(multimeter, neuron) 및 nest.Connect(neuron, spikerecorder) 총 두 번의 Connect를 호출하면 된다.
  - Connect(n1, n2)의 입력 인자의 순서는 중요하다. 기본적으로 n1 → n2로 향하는 신호 흐름의 방향을 의미하기 때문이다. 예시 코드들에서 multimeter는 neuron을 향해 측정값에 대한 request를 보내고, neuron은 spikerecorder로 spike가 발생했다는 신호를 보내기 때문에 위와 같은 순서로 쓰였다.

- nest.Simulate(t) 함수는 t 밀리초 동안 시뮬레이션을 실행하는 함수이다. 이 때 t는 double 타입임에 주의하자.


### Device에서 데이터 추출하고 그래프 그리기

- 시뮬레이션이 끝나면, device 노드 (예: multimeter, spikerecorder) 오브젝트에는 시뮬레이션 결과가 기록되어 있다. 이 기록 결과를 추출하기 위해 get() 메서드를 사용하면 된다. 예를 들면, multemeter 오브젝트에 대해 dmm = multemeter.get() 코드는 측정 결과를 dictionary 타입으로 반환한다. 이 오브젝트에는 events라는 이름의 단일한 entry가 존재하며, 여기에 대응되는 value에 다시 dictionary 타입으로 측정 결과 및 시간이 저장되어 있다.
  - 즉, 데이터 구조가 다음과 같다. {events: {V_m: times}}
  - 여기서 다시 개별 데이터를 받아오고 싶다면 다음과 같은 코드를 사용한다:
    - Vms = dmm["events"]["V_m"]
    - ts = dmm["events"]["times"]

- 결과를 plot하기 위해서는 매트랩에서와 비슷하게 plot()함수를 사용한다. 위에서 plt라는 이름으로 모듈을 import했다면, plt.plot(ts, Vms) 코드를 사용하면 시간에 따른 막전위의 변화를 plotting할 수 있다.
  - plot result를 실제로 보려면 plt.show() 함수를 쓴다. 만약 GUI를 지원하지 않는 환경이라면 plt.show() 후 plt.savefig('적당한파일명.png')와 같은 함수를 사용해 저장한 다음 GUI가 지원되는 환경에서 볼 수 있다. (이를테면 Windows 환경에서 CLI linux 가상 환경을 동시에 구동중인 경우...)

- 하나의 multimeter로 여러 개의 neuron의 결과를 측정하는 것 또한 가능하다. 예를 들면 새로운 뉴런 neuron2 = nest.Create("iaf_psc_alpha")를 형성하고 적당히 파라미터를 설정한 후, nest.Connect(multimeter, neuron2)를 사용해 아까 이미 neuron에 연결해둔 multimeter를 그대로 neuron2에도 연결할 수 있다.
  - 주의할 점은, 이 경우 측정한 결과를 분리하는 과정이 필요하다. multiple neuron을 하나의 multimeter로 측정하면 결과 array가 겹쳐서 저장된다. 위 예시의 경우 2개의 뉴런을 한꺼번에 측정했으므로, array의 짝수번 index (0, 2, 4, 8, ...)에는 1번 뉴런의 결과가 저장되어 있고 홀수번 index (1, 3, 5, 7, ...)에는 2번 뉴런의 결과가 저장되어 있다.
  - 예시: Vms1 = dmm["events"]["V_m"][0: 1: 2];Vms2 = dmm["events"]["V_m"][1: -1: 2]

- 여기까지의 결과물: [링크](https://github.com/froggo-roggo/froggo-nest-study/blob/main/myfirstnestproject.py)

### 특정한 연결로 노드 연결하기

- 실제 뉴런 및 시냅스 사이의 연결은 크게 '흥분성(excitatory)'과 '억제성(inhibitory)'의 두 종류로 나눌 수 있다. NEST에서는 이러한 연결들을 synapse 노드의 weight을 바꾸는 것으로 구현할 수 있다.

- 예를 들면, 푸아송 과정을 통해 모델링 된 두 종류의 연결 (흥분성 및 억제성)은 다음과 같이 모델링할 수 있다.

``` python
neuron = nest.Create("iaf_psc_alpha")
neuron.set(I_e = 0.0)
multimeter = nest.Create("multimeter")
multimeter.set(record_from = ["V_m"])
spikerecorder = nest.Create("spike_recorder")

noise_ex = nest.Create("poisson_generator") # excitatory spike train
noise_in = nest.Create("poisson_generator") # inhibitory spike train
noise_ex.set(rate=80000.0)
noise_in.set(rate=15000.0)

syn_dict_ex = {"weight": 1.2}
syn_dict_in = {"weight": -2.0}
nest.Connect(noise_ex, neuron, syn_spec=syn_dict_ex)
nest.Connect(noise_in, neuron, syn_spec=syn_dict_in)

nest.Connect(multimeter, neuron)
nest.Connect(neuron, spikerecorder)

```

[전체 코드](https://github.com/froggo-roggo/froggo-nest-study/blob/main/mysecondnestproject.py)

<img src = "https://github.com/froggo-roggo/froggo-nest-study/blob/main/exinsimresult.png">

### 두 개의 연결된 뉴런
- 두 뉴런을 연결할 때도 Connect 함수를 쓰면 된다.
  - 예
  ```python
  import nest
  neuron1 = nest.Create("iaf_psc_alpha")
  neuron1.set(I_e=376.0)
  neuron2 = nest.Create("iaf_psc_alpha")
  multimeter = nest.Create("multimeter")
  multimeter.set(record_from=["V_m"])
  
  nest.Connect(neuron1, neuron2, syn_spec = {"weight":20.0}) # 20의 weight로 연결한다는 뜻이 된다.
  nest.Connect(multimeter, neuron2)
  ```
  - 만약 뉴런 사이의 weight 이외에도 delay를 설정하고 싶다면,
  ```python
  nest.Connect(neuron1, neuron2, syn_spec={"weight":20.0, "delay":1.0})
  ```
  와 같이 사용하면 된다.

### 커맨드 정리