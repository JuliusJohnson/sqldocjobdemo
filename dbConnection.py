import pyodbc
SERVER = "Julius"
DATABASE= "Test"


def getJobs(jobName):
    conn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=Yes;Encrypt=Yes;TrustServerCertificate=YES;APP=SQL Server Job Report;')
    #conn = pyodbc.connect('Driver={ODBC Driver 18 for SQL Server};Server=test;UID=user;PWD=password;Encrypt=no;')

    cursor = conn.cursor()
    ### SQL QUERY START ###
    jobStepsSql= f'''  DECLARE @jobname varchar(100) 

  --SET @jobname = {jobName}

  IF @jobname = ''
	BEGIN
      SET  @jobname = '%';
	END;
    ELSE
        SET @jobname = @jobname;
    -- Insert statements for procedure here
SELECT Replace(sj.NAME, ' ', '_')  AS JobName,
       sj.enabled,
       sj.start_step_id,
	   sj.description,
       sjs.step_id,
       sjs.step_name,
       sjs.subsystem,
       sjs.command,
       CASE on_success_action
         WHEN 1 THEN 'Quit with success'
         WHEN 2 THEN 'Quit with failure'
         WHEN 3 THEN 'Go to next step'
         WHEN 4 THEN 'Go to step '
                     + Cast(on_success_step_id AS VARCHAR(3))
       END                         On_Success,
       CASE on_fail_action
         WHEN 1 THEN 'Quit with success'
         WHEN 2 THEN 'Quit with failure'
         WHEN 3 THEN 'Go to next step'
         WHEN 4 THEN 'Go to step '
                     + Cast(on_fail_step_id AS VARCHAR(3))
       END                         On_Failure,
       sj.delete_level,
       last_run_date,
       last_run_duration,
       last_run_outcome,
       'lastrunliteral' = Dateadd(millisecond, sjs.last_run_time,
                            CONVERT(DATETIME, Cast(
                                                 NULLIF(sjs.last_run_date, 0) AS
                                                 VARCHAR(
                                                 10)))),
       'lastrunday' = Datename(dw, Dateadd(millisecond, sjs.last_run_time,
                                                      CONVERT(DATETIME, Cast(
                                     NULLIF(sjs.last_run_date, 0) AS
                                     VARCHAR(10))))),
       'lastrundate' = CONVERT(CHAR, Dateadd(millisecond, sjs.last_run_time,
                                                         CONVERT(DATETIME, Cast(
                                       NULLIF(sjs.last_run_date, 0)
                                       AS VARCHAR(10)))), 9),
       CONVERT(DATE, CASE
                       WHEN Cast(last_run_date AS CHAR(8)) = 0 THEN NULL
                       ELSE Cast(last_run_date AS CHAR(8))
                     END, 101),
       last_run_duration / 10000   Hours,
       last_run_duration / 100%100 Minutes,
       last_run_duration%100       Seconds
FROM   msdb.dbo.sysjobs AS sj
       INNER JOIN msdb.dbo.sysjobsteps sjs
               ON sj.job_id = sjs.job_id
WHERE  Replace(sj.NAME, ' ', '_') LIKE ?'''
    ### SQL QUERY END ###
    cursor.execute(jobStepsSql, jobName)
    return cursor