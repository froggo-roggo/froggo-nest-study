## 파트 3: 시냅스로 네트워크 연결하기
- 원문: <a href="https://nest-simulator.readthedocs.io/en/stable/tutorials/pynest_tutorial/part_3_connecting_networks_with_synapses.html#pynest-tutorial-3">링크</a>
  - 안 중요한 내용은 적당히 뺐으니 정확한 내용은 반드시 원문을 참조

### 서론
- 이 섹션을 통해 배울 수 있는 내용은 다음과 같다.
  - 노드 생성 전 시냅스 모델 파라미터 설정하기
  - Customized 파라미터를 사용하여 시냅스 모델 정의하기
  - 연결 루틴에 시냅스 모델 사용하기
  - 연결 형성 후 시냅스 값 쿼리하기
  - 연결 도중 및 연결 이후에 시냅스 값 설정하기



### 시냅스 모델 파라미터 설정하기
- synapse_models 파라미터를 사용하여 사용 가능한 시냅스 모델의 종류를 확인할 수 있다.
- 시냅스 모델은 뉴런 모델과 비슷하게 파라미터를 설정할 수 있다. GetDefaults(model) 함수를 사용하면 기본 파라미터 세팅을 확인할 수 있고, SetDefaults(model, params) 함수를 사용하면 설정할 수 있다.
  ```python
  nest.SetDefaults("stdp_synapse",{"tau_plus": 15.0})
  ```
- 위와 같은 방식으로 시냅스를 생성하면, tau_plus만이 15.0의 값으로 설정되고 나머지는 standard 값을 따라간다.
- 또한 뉴런과 비슷하게, 시냅스 역시 CopyModel() 함수를 이용하여 복사할 수 있다.
  ```python
  nest.CopyModel("stdp_synapse","layer1_stdp_synapse",{"Wmax": 90.0})
  ```
- 위 예시를 실행하면, Models()를 호출했을 때 반환되는 list에 layer1_stdp_synapse 라는 이름을 가진 synapse 역시 등장하게 되며, 다른 built-in model 이름을 쓰는 곳에 똑같은 방식으로 쓸 수 있다.


#### STDP (spike timing dependent plasticity) 시냅스
- STDP 시냅스는 예외적으로 GetDefaults와 SetDefaults 함수로 파라미터를 바꿀 수 없다. 특성이 postsynaptic spike train에 따라서도 바뀌기 때문이다. 그러므로 STDP depressing window의 time constant는 postsynaptic neuron에서의 파라미터이다. 이는 다른 뉴런을 생성할 때와 마찬가지로, Create 시점에서 파라미터를 입력하거나 Set 메서드 등으로 parameterize 함으로써 파라미터를 설정할 수 있다.
  ```python
  nest.Create("iaf_psc_alpha", params={"tau_minus": 30.0})
  ```

### 시냅스 모델로 연결하기
- 각 시냅스 타입에 연관된 시냅스 모델 역시 synapse specification dictionary 내에 파라미터를 설정할 수 있다. 만약 synapse model에 대한 설정이 없다면, connection은 기본적으로 [static_synapse](https://nest-simulator.readthedocs.io/en/stable/ref_material/glossary.html#term-static_synapse) 모델을 사용한다.

### 시냅스 파라미터 분배
- 시냅스 파라미터는 Connect() 함수로 전달된 synapse directory 안에 들어있다. 만약 파라미터가 스칼라(상수)로 종의되어 있다면 모든 connection은 같은 파라미터를 이용해 생성된다. 또한, NEST의 Parameter 객체를 사용해 *랜덤*하게 분배할 수도 있다. Parameter 객체는 더 복잡한 파라미터를 만들기 위해 combine 될 수도 있다.
- 추가적으로, (확률) 분포를 사용하여 파라미터를 정의할 수도 있다. 예를 들면 균등하게 분포된 STDP 시냅스의 정의는 다음과 같이 이루어진다.
  ```python
  alpha_min = 0.1
  alpha_max = 2.
  w_min = 0.5
  w_max = 5.

  syn_dict = {"synapse_model": "stdp_synapse",
              "alpha": nest.random.uniform(min=alpha_min, max=alpha_max),
              "weight": nest.random.uniform(min=w_min, max=w_max),
              "delay": 1.0}
  nest.Connect(epop1, neuron, "all_to_all", syn_dict)
  ```
- 사용 가능한 분포의 종류는 [여기](https://nest-simulator.readthedocs.io/en/stable/synapses/connection_management.html#connection-management)에 있다. 대표적으로 다음과 같은 확률분포를 쓸 수 있다.

|분포 종류|정의 파라미터(Key)|비고|
|:---:|:---:|:---:|
|normal|mean, std|정규분포|
|lognormal|mean, std|로그정규분포|
|uniform|min, max|균등분포|
|exponential|beta|지수분포|
|gamma|kappa, theta|감마분포|

### 시냅스 쿼리
- 시냅스, 또는 연결 querying 할 때는 GetConnections(source = None, target = None, synapse_model = None)을 사용하면 주어진 specification에 맞는 연결 식별자 (SynapseCollection)을 반환한다. 아무런 argument도 입력하지 않았을 때 함수는 네트워크 상에 존재하는 모든 conenction을 반환한다.
- 만약 source가 특정되어 있다면, 함수는 해당 population (NodeCollection of one or more nodes)으로부터 나가는 모든 연결을 반환한다. 마찬가지로 target이 특정되어 있다면, 함수는 해당 population으로 향하는 모든 연결을 반환한다. synapse_model이 특정되어 있다면, 주어진 synapse model을 가진 연결을 반환한다.
  ``` python
  nest.GetConnections(epop1) # source is epop 1
  nest.GetConnections(target=epop2) # traget is epop 2
  nest.GetConnections(synapse_model="stdp_synapse") # find synapse that is stdp_synapse type
  ```
- target 및 synapse_model을 특정하는 것은 모든 연결을 살펴봐야 하기 때문에 source를 특정하는 것보다 오래 걸린다. 각각의 specification은 하나만 쓰거나 다른 것과 조합해서 쓸 수 있다.
- 주의할 점은, 상기한 querying 커맨드는 local connection만을 반환한다. ("Note that all these querying commands will only return the local connections, i.e. those represented on that particular MPI process in a distributed simulation." [참조](https://nest-simulator.readthedocs.io/en/stable/ref_material/glossary.html#term-MPI))
- 연결에 대한 식별자 SynapseCollection을 알고 있다면, get() 메서드를 사용해 데이터를 추출할 수 있다. 가장 단순한 경우 이 메서드를 실행하면 GetConnections()로 찾을 수 있는 각 연결들의 파라미터와 변수를 포함하는 list의 dictionary를 반환한다.
- 하지만 보통은 모든 정보를 필요로 하지는 않기 때문에 메서드의 argument로 string specificaiton을 넣어주면 된다.
  ``` python
  conns = nest.GetConnections(epop1, synapse_model="stdp_synapse")
  targets = conns.get("target")
  conn_vals = conns.get(["target","weight"]) # keys can be a list of keys as well.
  ```

### Coding style
[링크 참조](https://nest-simulator.readthedocs.io/en/stable/tutorials/pynest_tutorial/part_3_connecting_networks_with_synapses.html#coding-style)

자잘한 코드 작성 스타일에 관한 팁

### 커맨드 정리