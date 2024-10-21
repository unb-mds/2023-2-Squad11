import { Fragment } from 'react';
import ClassInfoBox from './ClassInfoBox';
import { ClassType, DisciplineType } from '@/app/utils/api/searchDiscipline';
import { FiChevronDown, FiChevronUp } from 'react-icons/fi';

interface DisciplineFragmentPropsType {
  index: number;
  discipline: DisciplineType;
  disciplineInfos: {
    searchedDisciplineInfos: Array<DisciplineType>;
    setSearchedDisciplineInfos: React.Dispatch<
      React.SetStateAction<DisciplineType[]>
    >;
  };
  handleSelectClass: (discipline: DisciplineType, cls: ClassType) => void;
}

function DisciplineFragmentJSX({
  handleDisciplineToggle,
  ...props
}: {
  handleDisciplineToggle: (index: number) => void;
  props: DisciplineFragmentPropsType;
}) {
  const { index, discipline, handleSelectClass } = props.props;

  return (
    <Fragment>
      <button
        onClick={() => handleDisciplineToggle(index)}
        aria-label="Expandir/Recolher disciplina"
        className="flex items-center gap-2 relative"
      >
        {discipline.expanded ? (
          <FiChevronUp size={18} />
        ) : (
          <FiChevronDown size={18} />
        )}

        <span className="font-semibold text-left">
          {discipline.name} - {discipline.code}
        </span>
      </button>
      {discipline.expanded && (
        <div className="flex flex-col gap-2">
          {discipline.classes.map((cls, index) => (
            <ClassInfoBox
              key={index}
              currentClass={cls}
              currentDiscipline={discipline}
              onClick={() => handleSelectClass(discipline, cls)}
            />
          ))}
        </div>
      )}
    </Fragment>
  );
}

export default function DisciplineFragment(props: DisciplineFragmentPropsType) {
  const { searchedDisciplineInfos, setSearchedDisciplineInfos } =
    props.disciplineInfos;

  function handleDisciplineToggle(index: number) {
    let newInfo: Array<DisciplineType> = [];
    searchedDisciplineInfos.forEach((discipline, number) => {
      if (number != index)
        newInfo.push({
          ...discipline,
          expanded: false,
        });
      else
        newInfo.push({
          ...discipline,
          expanded: !discipline.expanded,
        });
    });

    setSearchedDisciplineInfos(newInfo);
  }

  return DisciplineFragmentJSX({ handleDisciplineToggle, props });
}
