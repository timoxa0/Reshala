import commentjson as json
import os


class Dictionary:
    def __init__(self, dictfile):
        self.dictfile = dictfile
        if not os.path.exists(self.dictfile):
            with open(self.dictfile, 'w', encoding='utf-8') as file:
                json.dump(
                    {'внарушение контракта': '(слитно)', 'невзвалив': '(раздельно)', 'быстробыстро': '(дефис)', 'подетски': '(дефис)', 'прорешайка': '(раздельно)', 'заяцто убежал': '(раздельно)', 'звёздыто как сияют': '(дефис)', 'нескучно, а интересно': '(раздельно)', 'бубубу': '(дефис)', 'ему невдомёк': '(слитно)', 'комната непроветрена': '(раздельно)', 'что-то вроде кино': '(слитно)', 'скажи мне тоже, что и говорил': '(раздельно)', 'стоить недёшево': '(слитно)', 'баюбай': '(дефис)', 'ему невтерпёж': '(ничего)', 'эхма': '(раздельно)', 'приезжай вслед за мной': '(слитно)', 'нужно чемто заняться': '(дефис)', 'до сих пор несвязанная шаль': '(раздельно)', 'внутри трамвая': '(слитно)', 'воттебераз': '(дефис)', 'опустить наземь': '(слитно)', 'обратиться поповоду доклада': '(раздельно)', 'отстанька': '(дефис)', 'негреющее солнце': '(слитно)', 'страницы неизмяты': '(раздельно)', 'никого неудивляющий факт': '(раздельно)', 'поговорить насчёт репетиции': '(слитно)', 'всилу обстоятельств': '(раздельно)', 'недоставленное письмо': '(слитно)', 'занятьсято мне нечем': '(дефис)', 'неправильно, а с ошибкой': '(раздельно)', 'крайне недружелюбно': '(слитно)', 'делать нерадиво': '(слитно)', 'деньто был интересный': '(дефис)', 'выдать замуж': '(ничего)', 'яйца всмятку': '(раздельно)', 'вначале века': '(раздельно)', 'бежать вовсю': '(слитно)', 'в тоже время': '(раздельно)', 'снимика': '(дефис)', 'нехолодно, а жарко': '(раздельно)', 'отменить поход ввиду грозы': '(слитно)', 'покитайски': '(раздельно)', 'непроверив': '(раздельно)', 'что-то вроде домика': '(слитно)', 'стать друзьями навек': '(слитно)', 'сейчасто уж не успеешь': '(дефис)', 'уж поверьте': '(ничего)', 'непообедав': '(раздельно)', 'выставлять напоказ': '(раздельно)', 'нестись вскач': '(ничего)', 'сразуто мне не понять': '(раздельно)', 'помолочика': '(дефис)', 'отнюдь неинтересно': '(раздельно)', 'несоздав': '(раздельно)', 'охохо': '(дефис)', 'вчетвёртых': '(раздельно)', 'ойли': '(раздельно)', 'чтобы ни спросили, молчи': '(раздельно)', 'говорить напрямую': '(слитно)', 'невозмутимый тон': '(раздельно)', 'совершенно несерьёзно': '(слитно)', 'я тоже хочу на море': '(слитно)', 'попасть впросак': '(слитно)', 'город также красив, как и всегда': '(раздельно)', 'нестись вскачь': '(слитно)', 'одежда ещё несшита': '(раздельно)', 'несмотря на чувства': '(слитно)', 'крестнакрест': '(дефис)', 'влево от дороги': '(слитно)', 'спалить дотла': '(слитно)', 'ввиде звёздочки': '(раздельно)', 'крякать поутиному': '(дефис)', 'вцелях привлечения внимания': '(слитно)', 'эгеге': '(дефис)', 'рубить сплеча': '(раздельно)', 'заходите поодному': '(раздельно)', 'никем невыученное правило': '(раздельно)', 'отвечать поразному': '(дефис)', 'дзыньдзынь': '(дефис)', 'купить задаром': '(слитно)', 'посмотрика': '(дефис)', 'немедля с ответом': '(раздельно)', 'в чёмто он был не прав': '(дефис)', 'непросохшая после дождя земля': '(раздельно)', 'гулять неторопливо': '(слитно)', 'никем недоказанные факты': '(раздельно)', 'неверящий, а сомневающийся': '(раздельно)', 'лиш одно сомнение': '(ничего)', 'неустремившись': '(слитно)', 'наклейтека': '(дефис)', 'телефонто не звонил': '(дефис)', 'сделай также, как твой сосед': '(раздельно)', 'неглупо, а умно': '(слитно)', 'чтобы ты ни делал, не бойся': '(раздельно)', 'поучиська': '(дефис)', 'посредством перевода': '(слитно)', 'вместо учителя': '(слитно)', 'они кудато уехали': '(раздельно)', 'необозначенное на карте озеро': '(раздельно)', 'подружески': '(дефис)', 'вовремя отпуска': '(раздельно)', 'дада': '(дефис)', 'ввек не разобраться': '(слитно)', 'поотечески': '(дефис)', 'полечиська': '(дефис)', 'собираться впопыхах': '(слитно)', 'пропустить урок ввиду болезни': '(слитно)', 'поармянски': '(дефис)', 'Дождя также не ожидается.': '(слитно)', 'встать нацыпочки': '(раздельно)', 'я тоже это не сделал': '(слитно)', 'ему пришлось несладко': '(слитно)', 'взять безведома': '(раздельно)', 'неглядя': '(раздельно)', 'неубив медведя': '(раздельно)', 'использовать тоже название, что у них': '(раздельно)', 'попредъявлении паспорта': '(слитно)', 'незанавешенные окна': '(раздельно)', 'незакончившееся вовремя собрание': '(раздельно)', 'бибип': '(дефис)', 'поокончании года': '(слитно)', 'кваква': '(дефис)', 'воизменение распоряжения': '(раздельно)', 'вместето веселее': '(дефис)', 'обувь невымыта': '(раздельно)', 'спойка': '(дефис)', 'согласиться поневоле': '(слитно)', 'тьфутьфу': '(дефис)', 'лёгкуюто работу я сам сделаю': '(дефис)', 'случаи наподобие этого редки': '(слитно)', 'сделано насовесть': '(слитно)', 'втретьих': '(дефис)', 'сверх моего терпения': '(слитно)', 'нескроив': '(слитно)', 'выехать поутру': '(слитно)', 'перестанька': '(дефис)', 'сделать вотместку': '(раздельно)', 'вдвое меньше': '(слитно)', 'кормить наубой': '(раздельно)', 'сидеть наверху': '(слитно)', 'обманывать невыгодно': '(слитно)', 'потвоему мнению': '(дефис)', 'непользуясь льготами': '(раздельно)', 'заплатика': '(дефис)', 'впишика': '(дефис)', 'взять безспроса': '(раздельно)', 'непрояснившееся после бури небо': '(раздельно)', 'неделая': '(раздельно)', 'броситься наперехват беглецам': '(слитно)', 'нырнуть вглубь': '(слитно)', 'цокцок': '(дефис)', 'стоять неустойчиво': '(слитно)', 'ничего непонимающий зверёк': '(слитно)', 'втрое меньше': '(слитно)', 'не сегоднязавтра': '(дефис)', 'вспомника': '(дефис)', 'ничуть недоверчиво': '(слитно)', 'крайне неспокойно': '(слитно)', 'неповторяя': '(раздельно)', 'сделать помоему': '(дефис)', 'непререкаемый авторитет': '(слитно)', 'никак некончающийся день': '(раздельно)', 'посравнению с тобой': '(раздельно)', 'вместо перемены': '(слитно)', 'он тоже надел пальто': '(слитно)', 'встать надыбы': '(раздельно)', 'начника': '(дефис)', 'три дня кряду идёт дождь': '(слитно)', 'попусту тратить время': '(слитно)', 'вцелях получения прибыли': '(раздельно)', 'приехать издалека': '(слитно)', 'незамеченная учеником ошибка': '(слитно)', 'стоять внизу': '(раздельно)', 'успеть вовремя': '(раздельно)', 'неотдохнув': '(раздельно)', 'станцуйка': '(раздельно)', 'понемецки': '(дефис)', 'Допустить также, что ты не прав.': '(слитно)', 'воизбежание проблем': '(раздельно)', 'весьма небыстро': '(слитно)', 'коекуда': '(дефис)', 'неоглянувшись': '(раздельно)', 'нужно быть начеку': '(раздельно)', 'ничегото ты не понял': '(дефис)', 'зашейтека': '(дефис)', 'всё также льёт дождь, как вчера': '(раздельно)', 'выговор попричине опоздания': '(слитно)', 'невыученный урок': '(слитно)', 'письмо нераспечатано': '(раздельно)', 'броситься наперерез': '(слитно)', 'сыграй тоже, что и он': '(раздельно)', 'смотреть недоумевающе': '(слитно)', 'невызубренные, а понятые правила': '(раздельно)', 'сделать неплохо': '(слитно)', 'разделить надвое': '(слитно)', 'напротяжении многих лет': '(раздельно)', 'держала тоже самое одеяло': '(раздельно)', 'несделанное вовремя дело': '(раздельно)', 'подобрупоздорову': '(дефис)', 'очень неаккуратно': '(слитно)', 'всё попрежнему': '(дефис)', 'осторожен сверх меры': '(слитно)', 'непоблагодарив': '(раздельно)', 'хохохо': '(раздельно)', 'делиться побратски': '(дефис)', 'произойти неизбежно': '(слитно)', 'отнюдь неправильно': '(раздельно)', 'хочу, чтобы было лето': '(раздельно)', 'никем неусвоенное правило': '(слитно)', 'нерассмеявшись': '(раздельно)', 'както это неправильно': '(дефис)', 'приучика': '(дефис)', 'куку': '(раздельно)', 'иш какой шустрый': '(ничего)', 'неработая': '(раздельно)', 'неумывшись': '(слитно)', 'давнымдавно': '(дефис)', 'попрошествии лет': '(раздельно)', 'разрешить проблему похорошему': '(дефис)', 'егото я и хотел спросить': '(дефис)', 'далекодалеко': '(дефис)', 'ненаучившись': '(раздельно)', 'в пухипрах': '(раздельно)', 'порусски': '(раздельно)', 'Мне тоже купили платье.': '(слитно)', 'далеко невесело': '(раздельно)', 'попрежнему пути': '(раздельно)', 'неизданный при жизни роман': '(раздельно)', 'это вдвойне приятно': '(слитно)', 'в доме неуютно': '(слитно)', 'он тоже из дворянской семьи': '(слитно)', 'утром натощак': '(слитно)', 'рассказывать неинтересно': '(слитно)', 'вымыть дочиста': '(раздельно)', 'расти непрерывно': '(слитно)', 'хотеть выйти замуж': '(ничего)', 'повсюду виднеются цветы': '(слитно)', 'нескошенная трава': '(слитно)', 'выходить замуж': '(ничего)', 'кукареку': '(раздельно)', 'ушёл, непрощаясь': '(раздельно)', 'нырнуть неглубоко': '(слитно)', 'тутуту': '(дефис)', 'диньдон': '(дефис)', 'нежданнонегаданно': '(дефис)', 'мне невмоготу': '(слитно)', 'нисколько недалеко': '(раздельно)', 'поступить нелогично': '(раздельно)', 'ехать навстречу друг другу': '(слитно)', 'полюдски': '(дефис)', 'ненавидя': '(слитно)', 'пояпонски': '(дефис)', 'поприбытии в деревню': '(раздельно)', 'также любезен, как и всегда': '(раздельно)', 'покошачьи': '(дефис)', 'выглядеть неказисто': '(слитно)'},
                    file)

    def load(self) -> dict:
        with open(self.dictfile, 'r', encoding='utf-8') as file:
            return json.load(file)

    def dump(self, dictionary) -> None:
        with open(self.dictfile, 'w', encoding='utf-8') as file:
            json.dump(dictionary, file, indent=4)