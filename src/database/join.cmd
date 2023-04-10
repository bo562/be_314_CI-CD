@echo off
echo ------------------------------ >  all.sql
echo -- Tradie System Schema Script >>  all.sql
echo ------------------------------ >>  all.sql
echo.  >>  all.sql
echo.  >>  all.sql

for %%i in (*.sql) DO (
   if NOT %%i==all.sql (
      echo ------------------------------ >>  all.sql
      echo -- From: %%i >>  all.sql
      type %%i >>  all.sql
      echo.  >>  all.sql
      echo.  >>  all.sql
   )
)
