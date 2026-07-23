from crewai import Agent, Task, Crew, Process
from langchain_community.llms import Ollama
import subprocess

# 1. تحديد الموديل اللي بنستخدمه (العقل المدبر يعمل محلياً على جهازك)
local_llm = Ollama(model="llama3")

# 2. دالة قراءة سجلات النظام الحية (آخر 20 سطر من جهازك)
def get_live_logs(lines=20):
    try:
        # هذا السطر ينفذ أمر لينكس لسحب آخر السجلات
        result = subprocess.run(
            ['tail', '-n', str(lines), '/var/log/auth.log'], 
            capture_output=True, 
            text=True, 
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"حدث خطأ: تأكد أنك تشغل الكود بصلاحيات sudo. تفاصيل: {e}"
    except Exception as e:
        return f"حدث خطأ غير متوقع: {e}"

# سحب السجلات الحقيقية وحفظها في متغير
real_ssh_logs = get_live_logs(20)

# 3. صناعة أعضاء الفريق (الـ Agents)
# الموظف الأول: وظيفته يطلع الأرقام المهمة من السجل المزعج
log_parser = Agent(
    role='محلل بيانات أمنية (Tier 1)',
    goal='استخراج أرقام الـ IP وأسماء المستخدمين وأوقات الدخول من السجلات.',
    backstory='أنت محلل دقيق جداً، وظيفتك تنظيف البيانات المعقدة لسجلات النظام وإخراج الخلاصة منها بوضوح.',
    verbose=True, # لمراقبة طريقة تفكيره
    allow_delegation=False,
    llm=local_llm
)

# الموظف الثاني: وظيفته يكتشف نوع الهجوم بناءً على الأرقام
threat_intel = Agent(
    role='باحث تهديدات سيبرانية',
    goal='تحليل البيانات المستخرجة، تحديد ما إذا كان هناك هجوم، وتحديد نوعه (مثلا Brute Force) ومستوى خطورته.',
    backstory='أنت خبير في اكتشاف أنماط الهجمات السيبرانية وربط السلوك غير الطبيعي بالثغرات المعروفة.',
    verbose=True,
    allow_delegation=False,
    llm=local_llm
)

# الموظف الثالث: وظيفته يكتب التقرير النهائي ويعطي الحل
commander = Agent(
    role='قائد فريق الاستجابة للحوادث (Incident Responder)',
    goal='كتابة تقرير نهائي ومختصر للحادثة وإعطاء أوامر نظام Linux لصد الهجوم.',
    backstory='أنت قائد الفريق، تكتب تقارير احترافية تعتمد على الحقائق وتعطي حلول تقنية مباشرة مثل أوامر الجدار الناري.',
    verbose=True,
    allow_delegation=False,
    llm=local_llm
)

# 4. تحديد المهام بالترتيب
# المهمة الأولى: نعطيها للمحلل الأول مع سجلات جهازك الحية
parse_logs_task = Task(
    description=f'حلل سجلات النظام التالية واستخرج أرقام الـ IP وحالة الدخول (نجاح أو فشل): \n{real_ssh_logs}',
    expected_output='قائمة واضحة تحتوي على أرقام الـ IP المستخرجة وحالة كل محاولة دخول.',
    agent=log_parser
)

# المهمة الثانية: لباحث التهديدات (يستلم النتيجة تلقائياً من الأول)
analyze_threat_task = Task(
    description='راجع البيانات التي استخرجها زميلك، وحدد هل يوجد هجوم فعلي أو مجرد دخول طبيعي، وحدد مستوى الخطورة.',
    expected_output='تقييم أمني قصير يحدد نوع التهديد (إن وجد) ومستوى خطورته.',
    agent=threat_intel
)

# المهمة الثالثة: للقائد (يستلم النتيجة تلقائياً من الثاني)
generate_report_task = Task(
    description='بناءً على التقييم الأمني، اكتب تقرير رسمي عن الحالة. إذا كان هناك هجوم، اكتب أمر الجدار الناري (iptables أو ufw) لحظر المخترق.',
    expected_output='تقرير نهائي يحتوي على ملخص للحالة الأمنية، وأوامر حماية جاهزة للنسخ إذا لزم الأمر.',
    agent=commander
)

# 5. تجميع الفريق وتشغيلهم بالترتيب (Sequential)
soc_crew = Crew(
    agents=[log_parser, threat_intel, commander],
    tasks=[parse_logs_task, analyze_threat_task, generate_report_task],
    process=Process.sequential 
)

print("\nبدأ فحص النظام... الفريق يعمل الآن على تحليل سجلات جهازك:\n")
final_report = soc_crew.kickoff()

print("\n==================================")
print("### التقرير الأمني النهائي ###")
print("==================================\n")
print(final_report)