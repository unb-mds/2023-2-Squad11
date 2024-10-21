'use client';

import { ScheduleClassType } from '@/app/contexts/SchedulesContext';
import { HTMLProps, useEffect, useState } from 'react';
import { generateSpecialDates } from '../ClassInfo';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogTitle,
  DialogTrigger,
} from '../ui/dialog';
import { FiInfo } from 'react-icons/fi';

interface SchedulePropsType extends HTMLProps<HTMLDivElement> {
  schedules?: Array<ScheduleClassType>;
  preview?: boolean;
  toDownload?: boolean;
}

export default function Schedule({
  schedules,
  preview,
  toDownload,
  ...props
}: SchedulePropsType) {
  const [currentSchedule, setCurrentSchedule] = useState<
    Array<Array<ScheduleClassType>>
  >(new Array(6).fill(new Array(15).fill(null)));
  const uniqueTeachers = new Set<string>();

  const days = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'];
  const times = [
    '08:00 - 08:55',
    '08:55 - 09:50',
    '10:00 - 10:55',
    '10:55 - 11:50',
    '12:00 - 12:55',
    '12:55 - 13:50',
    '14:00 - 14:55',
    '14:55 - 15:50',
    '16:00 - 16:55',
    '16:55 - 17:50',
    '18:00 - 18:55',
    '19:00 - 19:50',
    '19:50 - 20:40',
    '20:50 - 21:40',
    '21:40 - 22:30',
  ];

  useEffect(() => {
    const baseSchedule = new Array(6);
    for (let i = 0; i < baseSchedule.length; i++) {
      baseSchedule[i] = new Array(15).fill(null);
    }

    function addClassToSchedule(scheduleStructure: ScheduleClassType) {
      const { schedule } = scheduleStructure;
      const splitSchedule = schedule.split(' ');

      splitSchedule.forEach((piece) => {
        const regex = /^(\d+)([MNT])(\d+)$/;
        const match = piece.match(regex);
        if (match) {
          const [, day, period, time] = match;

          for (let i = 0; i < day.length; i++) {
            const x = parseInt(day[i]) - 2;
            for (let j = 0; j < time.length; j++) {
              let y = parseInt(time[j]) - 1;

              if (period === 'T') y += 5;
              else if (period === 'N') y += 11;

              baseSchedule[x][y] = scheduleStructure;
            }
          }
        }
      });
    }

    if (schedules) {
      schedules.forEach((schedule) => addClassToSchedule(schedule));
      setCurrentSchedule(baseSchedule);
    }
  }, [schedules]);

  return (
    <div
      {...props}
      className={`${
        toDownload
          ? ' flex justify-end flex-row-reverse pt-10 tracking-[0.01px]'
          : ''
      } ${preview ? 'scale-[.3]' : ''}`}
      onClick={props.onClick}
    >
      <div className={`p-5 ${!toDownload ? 'm-auto' : ''} w-max`}>
        <div className="flex justify-end">
          <div className="w-40"></div>
          <div className="flex">
            {days.map((day, index) => (
              <div key={index} className="text-center w-28 m-[2px]">
                <p>{day}</p>
              </div>
            ))}
          </div>
        </div>
        <div className="flex flex-col">
          {times.map((time, timeIndex) => (
            <div className="flex" key={timeIndex}>
              <div className="flex justify-center items-center font-mono w-40">
                <p>{time}</p>
              </div>
              <div className="flex">
                {days.map((day, dayIndex) => (
                  <div
                    key={dayIndex}
                    className={`flex ${
                      toDownload ? 'pb-5 font-mono' : ''
                    } rounded-xl border border-[#9B9898] justify-center items-center w-28 h-8 m-[2px]`}
                  >
                    {currentSchedule[dayIndex] &&
                      currentSchedule[dayIndex][timeIndex] &&
                      currentSchedule[dayIndex][timeIndex].discipline.code}
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
      {!preview && (
        <div
          className={`flex flex-col w-max pl-10 pb-5 ${
            toDownload ? 'max-w-lg' : ''
          }`}
        >
          <ul className="list-disc">
            {schedules &&
              schedules.map((schedule, index) => {
                return (
                  <div className="p-1" key={index}>
                    <li>
                      <span
                        className={`font-semibold ${
                          toDownload ? 'font-mono' : ''
                        }`}
                      >
                        {schedule.discipline.code}
                      </span>{' '}
                      - {schedule.discipline.name} -{' '}
                      <span className={toDownload ? 'font-mono' : ''}>
                        ({schedule.classroom})
                      </span>
                    </li>
                    <span className="font-semibold">PROFESSORES:</span>
                    <ul className="list-inside">
                      {schedule.teachers.map((teacher, index) => {
                        if (uniqueTeachers.has(teacher)) return null;

                        uniqueTeachers.add(teacher);
                        return (
                          <li key={index}>
                            <p>{teacher}</p>
                          </li>
                        );
                      })}
                    </ul>
                    {schedule.special_dates.length ? (
                      <>
                        <span className="font-semibold pr-2">DATAS:</span>
                        {!toDownload ? (
                          <Dialog>
                            <DialogTrigger aria-label="Informações">
                              <FiInfo size={20} />
                            </DialogTrigger>
                            <DialogContent>
                              <DialogTitle>Horários</DialogTitle>
                              <DialogDescription>
                                {generateSpecialDates(
                                  schedule.special_dates,
                                  schedule.days
                                )}
                              </DialogDescription>
                            </DialogContent>
                          </Dialog>
                        ) : (
                          generateSpecialDates(
                            schedule.special_dates,
                            schedule.days
                          )
                        )}
                      </>
                    ) : null}
                  </div>
                );
              })}
          </ul>
        </div>
      )}
    </div>
  );
}
