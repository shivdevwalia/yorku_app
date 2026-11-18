import type { Course, Graph } from '../lib/api';

export default function CourseList({ graph, selected, onSelect }: { graph: Graph; selected: string; onSelect: (course: Course) => void }) {
  return <div className="course-list"><div className="list-heading"><span>COURSE / TITLE</span><span>CREDITS</span><span>DETAILS</span></div>{graph.nodes.map(course => <button className={'course-row' + (selected === course.id ? ' selected-row' : '')} key={course.id} onClick={() => onSelect(course)}><span><strong>{course.id}</strong><span>{course.title}</span><small>{graph.edges.filter(edge => edge.target === course.id).map(edge => edge.kind + ': ' + edge.source).join(' · ') || 'No extracted incoming references; requirements may remain unknown.'}</small></span><span>{course.credits || '—'}</span><span>{course.detailStatus === 'retrieved' ? 'View source rules ↗' : 'Unverified ↗'}</span></button>)}</div>;
}
