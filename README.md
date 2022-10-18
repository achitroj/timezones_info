# Show different timezones in a user friendly format

### Instructions for running or understanding the script:
1. Run the following command on a terminal after going to the root location of this project - `pip install -r requirements.txt` (This will install `pytz` and `requests` module of python)

2. You can run the script now. Check examples below.

3. The script takes 2 (optional) parameters, `match` and `offset`. `match` param is used to show only the timezones region which matches the string supplied to this argument. 
Similarly, `offset` will show the timezone regions, which matches the offset values passed.

4. **Note that these 2 parameters work in OR condition. That means, if both the parameters are passed, then any timezone which matches with either parameters, wil be shown.**

5. If `offset` argument is passed, then the script checks for daylight saving (`isdst` field of json data).
 If daylight saving for a region is ON, then UTC value is considered.
If daylight saving is OFF, then the offset value passed by user is considered for filtering.

6. Unit test cases can be run in Pycharm/any other python enabled editor, or can be run via
going to the project directory in a terminal and running the command - `python -m unittest unit_tests\test_show_timezones.py`
 
### Examples to run the script:

> python show_timezones.py -h  (to get help)
>
> python show_timezones.py  (show all timezones without filtering)
>
> python show_timezones.py --match Alaska
>
> python show_timezones.py --offset 2 
>
> python show_timezones.py --match Alaska --offset 10
>
> python show_timezones.py --match Alaska --offset -10
 
 
 # Some example outputs:
 
![output_ex1](https://user-images.githubusercontent.com/3242362/196507074-816119bf-76da-4c24-af6d-0d283876e458.png)


![output_ex2](https://user-images.githubusercontent.com/3242362/196507129-9616d686-bb17-4c1a-9fa9-30c10bf65519.png)


![output_ex3](https://user-images.githubusercontent.com/3242362/196507151-bd424a51-6b0c-4fe4-8327-6e4587812494.png)




