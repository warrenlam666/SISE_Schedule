# SISE_Schedule
## 这是一个基于python编写的可以用于从广州大学华软软件学院学生系统（SISE)导出ics格式日历数据文件的程序
特点：
* 只需输入学号密码等基本信息即可从sise导出数据，简单方便
* 导出的文件可用于Google 日历，outlook等软件的导入
<br>
<br>使用方法：<br><br>
     如要导出2018年度第一学期的课程表，可执行一下代码： 
     
     import sise
     sise.schedule(username='1740123321',password='123456789',year=2018,semester=1,openday='20180903')
     
     
     参数说明：
     * username:学号，类型为str
     * password:密码,类型为str
     * year:所要导出课程表的学期,类型为str
     * semester：所要导出课程表的学期，可取值为1或2，类型为int
     * openday:选中该学期的开学时间,如'20180903',类型为str
     
     
     联系方式：zifeng2014@hotmail.com
     
     
