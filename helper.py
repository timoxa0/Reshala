from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from yaspeller import check as ys_check
from selenium.common import exceptions
from colorama import Fore, init
from selenium import webdriver
from convert import clearStr
import commentjson as json
from time import sleep
from random import *
import syncdictctl
import logging
import dictctl
import sys
import os


def query_yes_no(question, default=None):
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default:
        prompt = " [Y/n] "
    elif not default:
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        ynchoice = input().lower()
        if default is not None and ynchoice == "":
            return valid[default]
        elif ynchoice in valid:
            return valid[ynchoice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no'\n")


init(autoreset=True)

pdict_file = dictctl.Dictionary('dict.json')
pdict = pdict_file.load()

def f(string):
    d = {'а́': 'а', 'о́': 'о', 'у́': 'у', 'э́': 'э', 'и́': 'и', 'я́': 'я', 'ю́': 'ю', 'ы́': 'ы', 'е́': 'е'}
    for i in d:
        string = string.replace(i, d[i])
    return string

def main(config):
    try:
        class ColorFormatter(logging.Formatter):
            fmt = config['advanced']['logfmt']

            FORMATS = {
                logging.DEBUG: Fore.GREEN + fmt + Fore.RESET,
                logging.INFO: Fore.WHITE + fmt + Fore.RESET,
                logging.WARNING: Fore.YELLOW + fmt + Fore.RESET,
                logging.ERROR: Fore.RED + fmt + Fore.RESET,
                logging.CRITICAL: Fore.BLUE + fmt + Fore.RESET
            }

            def format(self, record):
                log_fmt = self.FORMATS.get(record.levelno)
                formatter = logging.Formatter(log_fmt)
                return formatter.format(record)


        logger = logging.getLogger('Helper')
        ch = logging.StreamHandler()
        eval(f'logger.setLevel(logging.{config["advanced"]["logLevel"]})')
        eval(f'ch.setLevel(logging.{config["advanced"]["logLevel"]})')
        ch.setFormatter(ColorFormatter())
        logger.addHandler(ch)


        ys_logger = logging.getLogger('YaSpeller')
        ch = logging.StreamHandler()
        eval(f'ys_logger.setLevel(logging.{config["advanced"]["logLevel"]})')
        eval(f'ch.setLevel(logging.{config["advanced"]["logLevel"]})')
        ch.setFormatter(ColorFormatter())
        ys_logger.addHandler(ch)

        user_dict = syncdictctl.ServerDictionary()

        options = webdriver.ChromeOptions()

        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        for arg in ["--disable-blink-features=AutomationControlled",
                        "--log-level=3",
                        "--remote-allow-origins=*",
                        "--app=data:,",
                        "--silent",
                        "--guest"]:
            options.add_argument(arg)
        prefs = {"credentials_enable_service": False, "profile.password_manager_enabled": False}
        options.add_experimental_option("prefs", prefs)
        options.headless = False

        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )

        url = 'https://login.cerm.ru/'

        driver.get(url=url)

        loginInput = driver.find_element(By.ID, 'txtLogin')
        passwordInput = driver.find_element(By.ID, 'txtPass')
        loginBtn = driver.find_element(By.ID, 'login_button')

        loginInput.send_keys(config['basic']['login'])
        passwordInput.send_keys(config['basic']['password'])
        loginBtn.click()

        try:
            driver.find_element(By.XPATH, '//*[@id="do_pWelcome"]/div[3]/table/tbody/tr[2]/td[4]/a').click()
            logger.info('Clicked go to button')
        except:
            logger.info('Go to button not found')

        old_exercise_elements = []
        try:
            showHiddenBtn = driver.find_element(By.CLASS_NAME, 'inactiveToggle')
            showHiddenBtn.click()
            sleep(1)
            old_exercise_elements = driver.find_elements(By.CLASS_NAME, 'exerciseClosed')
            logger.info('Show all exercises button found and clicked')
        except:
            logger.info('Show all exercises button not found')

        try:
            exercise_elements = driver.find_elements(By.CLASS_NAME, 'exerciseOpen')
        except exceptions.ElementNotInteractableException:
            print('Exercises not found')
            os.system(f'taskkill /f /im {config["advanced"]["driver_process"]}')
            os.system(f'taskkill /f /im {config["advanced"]["chrome_process"]}')
            sys.exit(0)

        exercises = []
        for exercise_element in exercise_elements + old_exercise_elements:
            exercises.append(
                {
                    'name': exercise_element.find_element(By.CLASS_NAME, 'exercise-name-cell').text,
                    'type': exercise_element.text.split('\n')[3],
                    'startBtn': exercise_element.find_element(By.CLASS_NAME, 'exercise__playBtn')
                }
            )
        for i in range(len(exercises)):
            print(f'[{i}] {exercises[i]["name"]} {exercises[i]["type"]}')

        while True:
            try:
                exercise = exercises[int(input('Select: '))]
                exercise['startBtn'].click()
                break
            except IndexError:
                pass
            except ValueError:
                pass
            except KeyboardInterrupt:
                logger.critical('Exitting...')
                os.system(f'taskkill /f /im {config["advanced"]["driver_process"]}')
                os.system(f'taskkill /f /im {config["advanced"]["chrome_process"]}')
                sys.exit(0)

        word = None
        while True:
            try:
                driver.find_element(By.CLASS_NAME, 'btn_yellow').click()
            except exceptions.NoSuchElementException:
                pass
            except exceptions.ElementNotInteractableException:
                pass

            try:
                sleep(1.5)
                raw_word = driver.execute_script('return window.document.getElementById(\'trainer_question\').innerHTML')
                word = f(raw_word.replace('<span class="word_hole"></span>', '*').replace('<span>́</span>', ''))
                logger.info(f'Word is: {word}')
                e_variants = driver.find_elements(By.CLASS_NAME, 'trainer_variant')
                t_variants = []
                for i in range(len(e_variants)):
                    t_variants.append(
                        {
                            'element': e_variants[i],
                            'text': e_variants[i].text.replace('(ничего)', '').replace('(слитно)', '').replace('(раздельно)', ' ').replace('(дефис)', '-')
                        }
                    )

                udict = user_dict.load() if config['dictionary']['use'] else {}
                if word in udict:
                    ans = udict[word]
                elif word.replace('*', '') in pdict:
                    ans = pdict[word.replace('*', '')].replace('(ничего)', '').replace('(слитно)', '').replace('(раздельно)', ' ').replace('(дефис)', '-')
                else:
                    r = randint(0, 1)
                    ys_query = word.replace('*', t_variants[r]['text'])
                    ys_response = ys_check(ys_query, lang='ru')
                    tmp = user_dict.load()
                    ys_logger.debug(f'Speller query: {ys_query}')
                    ys_logger.debug(f'Speller response: {ys_response.first_match()}/{ys_response.is_ok}')
                    if ys_response.is_ok:
                        ans = t_variants[r]['text']
                    else:
                        ans = t_variants[1 if r == 0 else 0]['text']

                for variant in t_variants:
                    if variant['text'] == ans:
                        variant['element'].click()

                if ans == ' ':
                    ans = '[_]'
                elif ans == '':
                    ans = '[]'

                logger.info(f'Answer is: {ans}')

            except exceptions.JavascriptException:
                try:
                    rno_right = f(driver.find_element(By.ID, 'trainer_rno_right').text)
                    logger.warning('Incorrect answer!')
                    for i in range(1, 4):
                        rno_input = driver.find_element(By.ID, 'prno')
                        rno_input.send_keys(rno_right)
                        sleep(randint(config['basic']['downlimit'] * 1000000, config['basic']['toplimit'] * 1000000) / 1000000)

                    if (word is not None) and (config['dictionary']['use']):
                        tmp = user_dict.load()
                        tmp[word] = clearStr(rno_right, word.replace('*', ''))
                        logger.info('Added to user dictionary')
                        logger.debug(f'User dict size: {len(tmp)}')
                        user_dict.dump(tmp)
                        tmp = None
                except exceptions.NoSuchElementException:
                    try:
                        resumeBtn = driver.find_element(By.CLASS_NAME, 'button btn_yellow')
                        exitBtn = driver.find_element(By.CLASS_NAME, 'button btn_grey_border')
                        if bool(config['advanced']['Always Continue']):
                            resumeBtn.click()
                        else:
                            if query_yes_no('Continue?', False):
                                resumeBtn.click()
                            else:
                                exitBtn.click()
                                break
                    except exceptions.NoSuchElementException:
                        pass

                except ValueError as ex:
                    logger.exception('Error occurred')

            except exceptions.TimeoutException:
                pass

            except exceptions.WebDriverException:
                logger.critical('Chrome closed unexpectedly! Cannot continue!')
                driver.quit()
                sys.exit(-1)

            except exceptions.NoSuchWindowException:
                logger.critical('Chrome closed unexpectedly! Cannot continue!')
                driver.quit()
                sys.exit(-1)

            except KeyboardInterrupt:
                logger.critical('Exitting...')
                os.system(f'taskkill /f /im {config["advanced"]["driver_process"]}')
                os.system(f'taskkill /f /im {config["advanced"]["chrome_process"]}')
                sys.exit(0)

            except Exception as ex:
                logger.exception('Error occurred')

        os.system(f'taskkill /f /im {config["advanced"]["driver_process"]}')
        os.system(f'taskkill /f /im {config["advanced"]["chrome_process"]}')
    
    except KeyboardInterrupt:
        logger.critical('Exitting...')
        os.system(f'taskkill /f /im {config["advanced"]["driver_process"]}')
        os.system(f'taskkill /f /im {config["advanced"]["chrome_process"]}')
        sys.exit(0)

if __name__=='__main__':
    with open('config.json', 'r') as file:
        config = json.load(file)
    main()
