## 파트 2: 뉴런 군집
- 원문: <a href="https://nest-simulator.readthedocs.io/en/stable/tutorials/pynest_tutorial/part_2_populations_of_neurons.html#pynest-tutorial-2">링크</a>
  - 안 중요한 내용은 적당히 뺐으니 정확한 내용은 반드시 원문을 참조

### 서론
- 이 섹션을 통해 배울 수 있는 내용은 다음과 같다.
  - 여러 파라미터를 이용해 뉴런 군집 만들기
  - 노드 생성 전 모델 파라미터를 설정하기
  - Customized 파라미터를 사용하여 모델 정의하기
  - 노드 생성 후 파라미터 randomize하기
  - 군집 간 random connection 만들기
  - device가 동작하거나 정지하도록 설정하고, 데이터를 파일에 저장하기
  - 시뮬레이션 reset하기



### 파라미터를 이용해 군집 노드 만들기
- Create 함수의 세 파라미터 중, 맨 앞의 'model'은 새로 만들어질 노드에 사용될 모델을 결정하는 인자로 반드시 필요한 (mandatory) parameter이다. 한편 두 번째와 세 번째인 n 및 params는 optional 인자이다. 먼저 n은 한 번에 생성할 노드의 개수를 지정하는 인자로, 아무것도 입력하지 않았을 때의 기본값은 1이고 자료형은 *integer*이다. 그리고 params는 노드를 초기화할 때 사용하는 파라미터를 지정하는 인자로, dictionary의 형태로 입력하면 된다.
  - **노드를 생성함과 동시에 노드 파라미터를 설정하는 것은 SetStatus() 또는 set() 메서드를 이용하는 것보다 효율적**이기 때문에 가능한 한 이용하는 것이 좋다.

- SetDefaults(model, params) 함수를 이용하면 **Create 함수를 사용하기 전에 노드 파라미터를 미리 설정**해둘 수 있다.
  - 이 파라미터는 하나의 model에 대해 계속 유효하다.
  - 예
  ```python
    ndict = {"I_e": 200.0, "tau_m": 20.0}
    nest.SetDefaults("iaf_psc_alpha", ndict)
    neuronpop1 = nest.Create("iaf_psc_alpha", 100)
    neuronpop2 = nest.Create("iaf_psc_alpha", 100)
    neuronpop3 = nest.Create("iaf_psc_alpha", 100)
  ```
  - "iaf_psc_alpha" 모델에 대해 SetDefault를 호출했으므로, 이후에 호출되는 모든 iaf_psc_alpha 뉴런들의 모델 파라미터 기본값이 ndict로 설정되었다.
  - 설정되지 않은 것은 군집 내 노드 개수(n)이므로, 여기서는 각 군집 당 100개의 노드가 포함되도록 설정했다.


- 만약 뉴런 군집이 같은 모델을 사용하지만 서로 다른 파라미터를 써야 하는 경우, CopyModel을 이용해 customized 모델 이름을 만들 수 있다.
  - 모델 이름(*string*)은 곧 모델 자체의 식별자이므로, 이름을 새로 만드는 것은 해당 세션 내에서 계속 유효한 사용자의 고유한 customized model 자체를 만드는 것을 의미한다.
  - 예 1
    ```python
    edict = {"I_e": 200.0, "tau_m": 20.0} # Parameter default value dictionary setting
    nest.CopyModel("iaf_psc_alpha", "exc_iaf_psc_alpha") # "exc_iaf_psc_alpha" is a new customized model forked from iaf_psc_alpha, a predefined, built-in model in NEST.
    nest.SetDefaults("exc_iaf_psc_alpha", edict) # And then set default values for the customized model
    
    ```
  - 예 2
    ```python
    idict = {"I_e": 300.0} # Parameter default value dictionary setting
    nest.CopyModel("iaf_psc_alpha", "inh_iaf_psc_alpha", params = idict) # Fork and set default in one line
    ```
  - 두 방법 모두 default를 설정한 이후에 Create하는 모든 노드들은 model name과 population number만 설정하면 된다. (이는 다수의 군집 노드를 만들고자 할 때 편리하다.)
    ```python
    epop1 = nest.Create("exc_iaf_psc_alpha", 100)
    epop2 = nest.Create("exc_iaf_psc_alpha", 100)
    ipop1 = nest.Create("inh_iaf_psc_alpha", 30)
    ipop2 = nest.Create("inh_iaf_psc_alpha", 30)
    ```

- 뿐만 아니라, 하나의 군집 노드에 포함된 요소들이 서로 다른(inhomogeneous) 파라미터를 각각 갖게 하는 것 또한 가능하다.
  - 파라미터로 설정하는 dictionary의 value로, scalar value 대신, 이후에 Create할 population의 number와 똑같은 길이의 list를 넣는다.
  - value로 단일한 scalar value를 넣으면 모든 뉴런에 대해서 적용하겠다는 뜻이 된다.
  - 예
    ```python
    parameter_dict = {"I_e": [200.0, 150.0], "tau_m": 20.0, "V_m": [-77.0, -66.0]}
    pop3 = nest.Create("iaf_psc_alpha", 2, params=parameter_dict)

    print(pop3.get(["I_e", "tau_m", "V_m"])) # able to check customized parameters of all neurons in the population
    ```


### 생성된 군집 노드의 파라미터 설정하기 (+ randomization)
- 항상 Create와 함께 파라미터를 설정할 수 있는 것은 아니기 때문에, 기본값을 사용해 군집 노드를 생성한 이후에도 개별 노드의 parameter를 바꾸는 것이 가능하다.
  - 튜토리얼 1에서와 마찬가지로 set() 메서드나 SetStatus() 함수로 개별 노드의 파라미터를 언제든지 수정할 수 있다.
    ```python
    Vth=-55. # fixed threshold
    Vrest=-70. # fixed resting potential
    dVms =  {"V_m": [Vrest+(Vth-Vrest)*numpy.random.rand() for x in range(len(epop1))]} # randomize initial membrane potential
    epop1.set(dVms) # set the membrane potential values for each neuron in epop1
    ```
  - 이 과정은 NEST의 내장 distrubition을 사용하여 epop1.set({"V_m": Vrest + nest.random.uniform(0.0, Vth-Vrest)})와 같이 한 줄로 나타낼 수 있다.
    - 단, 코드는 대부분의 경우 함축할수록 복잡해지고 관리도 어렵다는 점에 주의하자...



### 생성된 군집 간 Connection 만들기
- [결정론적 연결과 확률론적 연결을 포함해, 다양한 종류의 connection rule은 여기 참조](https://nest-simulator.readthedocs.io/en/stable/synapses/connection_management.html#connection-rules)

#### 1. 결정론적 연결 (deterministic connection)
- Connect(pre, post, conn_spec = None, syn_spec = None, return_synapsecollection = False) 함수는 세 번째 인자로 connectivity pattern을 지정하는 식별자를 받는다. 이 식별자는 string일 수도 있고 dictionary일 수도 있다.
  - 만약 아무것도 지정되지 않았다면, 기본값은 "all_to_all"로, 두 노드(각각 n, m개의 요소를 가진다고 가정) 사이에 가능한 모든 연결(n&#42;m개)을 만든다.
  - "one_to_one"으로 설정하면, 서로 크기가 n으로 같은 두 population에 대해, 순서대로 모든 요소들을 서로 짝지어서 n개의 연결이 생긴다.
  - multimeter 또한 비슷한 rule로 연결할 수 있다.

#### 2. 확률론적 연결 (random connection with probability)
- 보통 하나의 네트워크 내에서 생성되는 연결은 all-to-all보다 sparse하고, one-to-one보다 임의적이다. 따라서 다양한 종류의 분포 specification을 이용하여 노드 및 노드에 포함된 요소들 사이의 임의적 연결을 정의할 수 있다.
- indegree와 outdegree는 시냅스 전후 뉴런들에서 출발하거나 도착하는 connection의 수를 제한한다.
  - 예
    ```python
    d = 1.0
    Je = 2.0
    Ke = 20
    Ji = -4.0
    Ki = 12
    conn_dict_ex = {"rule": "fixed_indegree", "indegree": Ke}
    conn_dict_in = {"rule": "fixed_indegree", "indegree": Ki}
    syn_dict_ex = {"delay": d, "weight": Je}
    syn_dict_in = {"delay": d, "weight": Ji}
    nest.Connect(epop1, ipop1, conn_dict_ex, syn_dict_ex)
    # note that the population number n of epops and ipops are different
    # therefore the number of all possible connection between the nodes is 100 * 30 = 3000
    nest.Connect(ipop1, epop1, conn_dict_in, syn_dict_in)
    # epop1 and ipop1 are being pre and post to each other simultaneously.
    # this is legitimate for every conenctivity rule in NEST.
    ```
    - 여기서 indegree는 postsynaptic neuron으로 향하는 conneciton의 총 개수를 의미한다. 즉, fixed_indegree는 randomized된 전체 connection 중에서도 postsynaptic neuron으로 향하는 conenction 수를 제한한다는 뜻이 된다.
    - 반대로 outdegree는 presynaptic neuron에서 나오는 connection의 총 개수를 의미한다.
    - 대부분의 경우 (가능하다면) fixed_indegree를 설정하는 편이 더 효율적이다.
  - 한편 fixed_total_number connection은 pre와 post 군집에 있는 뉴런들을 무작위로 선택해 총 n개의 연결을 만든다.
  - ~~세 개 차이가 구체적으로 뭔지는 공부 좀 더 해야겄다... 어차피 방향이 항상 pre → post면 결국 같지 않나???~~

- pairwise_bernoulli 분포를 선택하면, 노드 사이에 가능한 모든 연결 중에서, 확률 p에 따라 몇몇 연결만을 선택한다.
  - 참조: 베르누이 분포는 p의 확률로 1 이고 1-p의 확률로 0인 확률변수의 분포로, 가능한 모든 연결의 개수(n&#42;m)가 충분히 많을 때 실제로 작동하는 연결의 수의 기댓값은 n&#42;m&#42;p개이다.

- conn_spec의 인자로 connectivity pattern을 지정하는 것 이외에도 self-connection이나 두 뉴런 간 중복 연결에 대한 설정을 바꿀 수 있다.
  - 식별자 dictionary에서, key "allow_autapses"(자기 연결)와 "allow_multapses"(중복 연결)에 대해 value로 False 혹은 True의 boolean value를 지정하면 된다.

- 마지막으로, 모든 connectivity rule에 대해 한 군집 노드가 pre와 post의 역할을 동시에 수행하는 것이 가능하다.



### Device의 행동 지정하기
- 모든 device는 기본적인 timing capacity를 가지고 있다.
  - 모든 시각은 origin(기본값 0)에 대해 상대적이다.
  - start (기본값 0)은 device가 행동을 시작하는 시각을 정의한다.
  - stop (기본값 ∞, 즉 시뮬레이션이 끝날 때까지)은 device가 행동을 끝내는 시각을 정의한다.
  - 예: 100 ms부터 150 ms까지만 작동하는 [포아송 생성기](https://nest-simulator.readthedocs.io/en/stable/models/poisson_generator.html)
    ```python
    pg = nest.Create("poisson_generator")
    pg.set({"start": 100.0, "stop": 150.0})
    ```
- 또한, 측정 device가 내놓는 result에 포함된 값 중 "events"를 추출하여 파일에 저장할 수 있다.
  - 측정이 길고 측정 대산 노드의 규모가 클수록, 파일에 따로 저장하는 편이 좋다.
  - 모든 측정 device는 data를 어디에 어떤 형식으로 저장할지에 대한 파라미터(record_to)를 받을 수 있다.
    - "ascii"는 측정 데이터를 파일로 dump한다.
    - "screen"은 측정 데이터를 화면에 띄운다.
    - "memory"는 측정 데이터를 메모리에 hold한다. (모든 측정 device에서 기본값)
  - 또한 이 데이터에 대한 label을 지정할 수 있는데, 따로 지정하지 않는다면 NEST에 의해 생성되는 기본값은 device id이다.
    - 만약 simulation이 다중 스레드 및 프로세스에서 진행되고 있다면, 각각의 스레드와 프로세스에 대해 파일이 하나씩 생성된다.
  - [측정 device에 대한 더 많은 내용은 이곳을 참조](https://nest-simulator.readthedocs.io/en/stable/devices/record_from_simulations.html#record-simulations)


여기까지 [전체 코드](https://github.com/froggo-roggo/froggo-nest-study/blob/main/neuronpopulation/populationsetting.py)


### 시뮬레이션 reset하기
- 만족할 만한 결과를 얻을 때까지 시뮬레이션을 반복해야 하는 경우, ResetKernel() 함수를 사용하면 한 프로세스 내에서 만든 모든 node와 customized model을 제거하고, internal clock을 0으로 초기화한다.
- 서로 다른 parameter setting으로 같은 simulation을 여러 번 반복할 때는, 모든 것을 reset할 필요 없이 그냥 반복문을 사용하고 반복마다 parameter setting만 update되도록 하는 것으로도 충분하다.



### Command overview


