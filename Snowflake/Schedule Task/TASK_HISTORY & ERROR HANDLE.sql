select *
  from table(information_schema.task_history())
  WHERE NAME ='CUSTOMER_TASK_PROCEDURE'
  order by scheduled_time;


  select *
  from table(information_schema.task_history(
  SCHEDULED_TIME_RANGE_START => DATEADD('HOUR',-2 ,CURRENT_TIMESTAMP),
  SCHEDULED_TIME_RANGE_END => DATEADD('HOUR',-1 ,CURRENT_TIMESTAMP),
  RESULT_LIMIT => 5,
  TASK_NAME => 'CUSTOMER_TASK_PROCEDURE'
  ))
  order by scheduled_time;