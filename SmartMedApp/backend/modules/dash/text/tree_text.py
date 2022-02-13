markdown_tree_graph = '''
    gini - Индекс Джини, также известный как загрязнение  Джини, вычисляет величину вероятности определенного признака,
    который классифицируется неправильно при случайном выборе. Если все элементы связаны с одним классом,
    то его можно назвать чистым.
    
    samples - Количество прошедших через этот узел образцов.
    
    value - Отношение классов, прошедших через этот узел, выраженное в абсолютных числах.
    
    class - Преобладающий класс.
    
    цвет - Отображает class. Чем ярче, тем больше преобладает class.
'''

markdown_results_table = '''
    Классификационная таблица, в которой наблюдаемые показатели принадлежности к группе противопоставляются
    предсказанным на основе рассчитанной модели. 
'''

markdown_quality = '''
    Accuracy - доля правильных ответов. Вероятность того, что класс будет предсказан правильно.
    
    Энтропийный индекс неоднородности - индекс, принимающий наибольшее значение  при равенстве долей классов,
                                        а наименьшее - при принадлежности всех объектов к классу.
                                        
    Индекс Джини - измеряет неравенство между значениями переменной. Чем выше значение индекса,
                   тем более рассредоточенными являются данные.
                   
    Индекс ошибочной классификации - достигает минимальное значение при принадлежности всех объектов обучающей выборке 
                                     к одному классу.
                                     
    Полнота - это доля найденных классфикатором объектов принадлежащих классу относительно всех объектов
              этого класса в тестовой выборке.
              
    Точность - это доля объектов действительно принадлежащих данному классу относительно всех документов,
               которые модель отнесла к этому классу.
               
    F1-мера - гармоническое среднее между точностью и полнотой. Она стремится к нулю,
              если точность или полнота стремится к нулю.
              
'''
