import { useMemo } from 'react';
import type { Course, Graph } from '../lib/api';

export default function PrerequisiteMap({ graph, selected, onSelect }: { graph: Graph; selected: string; onSelect: (course: Course) => void }) {
  const layout = useMemo(() => {
    const groups = new Map<number, Course[]>();
    graph.nodes.forEach(course => {
      const level = Math.min(5, Math.max(0, Math.floor(Number(course.number) / 1000)));
      groups.set(level, [...(groups.get(level) || []), course]);
    });
    const levels = [...groups.keys()].sort((first, second) => first - second);
    const positions = new Map<string, { left: number; top: number }>();
    levels.forEach((level, column) => groups.get(level)!.forEach((course, row) => positions.set(course.id, { left: column * 244 + 20, top: row * 96 + 60 })));
    return { levels, positions, width: Math.max(730, levels.length * 244 + 20), height: Math.max(430, ...[...groups.values()].map(group => group.length * 96 + 90)) };
  }, [graph]);
  const connected = new Set(graph.edges.filter(edge => edge.source === selected || edge.target === selected).flatMap(edge => [edge.source, edge.target]));
  return <div className="map-scroll" tabIndex={0} role="region" aria-label="Scrollable prerequisite reference map. Use the list view for equivalent text navigation.">
    <div className="map-canvas" style={{ width: layout.width, height: layout.height }}>
      {layout.levels.map((level, index) => <div className="level-label" key={level} style={{ left: index * 244 + 20 }}>{level === 5 ? '5000+ LEVEL' : level + '000 LEVEL'}</div>)}
      <svg className="map-lines" width={layout.width} height={layout.height} aria-hidden="true">
        <defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor" /></marker></defs>
        {graph.edges.map((edge, index) => {
          const source = layout.positions.get(edge.source), target = layout.positions.get(edge.target);
          if (!source || !target) return null;
          const start = source.left + 202, end = target.left;
          const sameColumn = source.left === target.left;
          const bend = sameColumn ? start + 25 : (start + end) / 2;
          const finish = sameColumn ? target.left + 202 : end;
          const path = 'M ' + start + ' ' + (source.top + 34) + ' C ' + bend + ' ' + (source.top + 34) + ', ' + bend + ' ' + (target.top + 34) + ', ' + finish + ' ' + (target.top + 34);
          return <path key={edge.source + edge.target + index} d={path} className={edge.kind + (edge.source === selected || edge.target === selected ? ' highlight' : '')} markerEnd="url(#arrow)" />;
        })}
      </svg>
      {graph.nodes.map(course => <button key={course.id} className={'map-node' + (selected === course.id ? ' selected' : '') + (connected.has(course.id) ? ' connected' : '') + (course.faculty !== 'LE' ? ' external' : '')} style={layout.positions.get(course.id)} onClick={() => onSelect(course)} aria-pressed={selected === course.id} title={course.id + ': ' + course.title}><strong>{course.id.split('/').slice(1).join('/')}</strong><span>{course.title}</span><small>{course.detailStatus === 'unresolved' ? 'Unresolved reference' : course.faculty !== 'LE' ? 'Supporting course' : (course.credits || '?') + ' credits'}</small></button>)}
    </div>
  </div>;
}
