import pyodbc
SERVER = "Julius"
DATABASE= "Test"


def getJobs(jobName):
    conn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=Yes;Encrypt=Yes;TrustServerCertificate=YES;APP=SQL Server Job Report;')
    #conn = pyodbc.connect('Driver={ODBC Driver 18 for SQL Server};Server=test;UID=user;PWD=password;Encrypt=no;')

    cursor = conn.cursor()
    ### SQL QUERY START ###
    jobStepsSql= f'''  DECLARE @jobname varchar(100) 

  SET @jobname = {jobName}

  IF @jobname = ''
	BEGIN
      SET  @jobname = '%';
	END;
    ELSE
        SET @jobname = @jobname;
    -- Insert statements for procedure here
    SELECT sj.name AS JobName,
           sj.enabled,
           sj.start_step_id,
           sjs.step_id,
           sjs.step_name,
           sjs.subsystem,
           sjs.command,
           CASE on_success_action
               WHEN 1 THEN
                   'Quit with success'
               WHEN 2 THEN
                   'Quit with failure'
               WHEN 3 THEN
                   'Go to next step'
               WHEN 4 THEN
                   'Go to step ' + CAST(on_success_step_id AS VARCHAR(3))
           END On_Success,
           CASE on_fail_action
               WHEN 1 THEN
                   'Quit with success'
               WHEN 2 THEN
                   'Quit with failure'
               WHEN 3 THEN
                   'Go to next step'
               WHEN 4 THEN
                   'Go to step ' + CAST(on_fail_step_id AS VARCHAR(3))
           END On_Failure,
           sj.delete_level,
           last_run_date,
           last_run_duration,
           last_run_outcome
    FROM msdb.dbo.sysjobs AS sj
        INNER JOIN msdb.dbo.sysjobsteps sjs
            ON sj.job_id = sjs.job_id
    WHERE sj.name LIKE @JobName'''
    ### SQL QUERY END ###
    cursor.execute('EXEC Test.dbo.proc_JobSteps @jobname = ?', jobName)
    return cursor