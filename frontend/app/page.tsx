'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { api, type Course, type Graph, type Meta, type Program } from '../lib/api';
import PrerequisiteMap from './PrerequisiteMap';
import CourseDetail from './CourseDetail';
import CourseList from './CourseList';

const EMPTY_GRAPH: Graph = { nodes: [], edges: [], total: 0, semantics: '' };

export default function Home() {
  const [meta, setMeta] = useState<Meta | null>(null);
  const [programs, setPrograms] = useState<Program[]>([]);
  const [programId, setProgramId] = useState('');
  const [supporting, setSupporting] = useState(true);
  const [subject, setSubject] = useState('EECS');
  const [search, setSearch] = useState('');
  const [courses, setCourses] = useState<Course[]>([]);
  const [graph, setGraph] = useState<Graph>(EMPTY_GRAPH);
  const [selected, setSelected] = useState<Course | null>(null);
  const [focus, setFocus] = useState('');
  const [view, setView] = useState<'map' | 'list'>('map');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [retry, setRetry] = useState(0);

  useEffect(() => {
    const controller = new AbortController();
    Promise.all([api<Meta>('meta', controller.signal), api<{ programs: Program[] }>('programs', controller.signal)])
      .then(([nextMeta, data]) => {
        if (nextMeta.schemaVersion !== '1') throw new Error('Unsupported catalogue API version. Update frontend and backend.');
        setMeta(nextMeta); setPrograms(data.programs);
      }).catch(cause => { if (!controller.signal.aborted) { setError(String(cause.message)); setLoading(false); } });
    return () => controller.abort();
  }, [retry]);

  useEffect(() => {
    if (!meta) return;
    const controller = new AbortController();
    const timer = setTimeout(() => {
      setLoading(true); setError('');
      const query = new URLSearchParams({ program: programId, supporting: String(supporting), q: search, subject });
      const graphQuery = new URLSearchParams(query);
      if (focus) graphQuery.set('focus', focus);
      Promise.all([api<{ courses: Course[] }>('courses?' + query, controller.signal), api<Graph>('graph?' + graphQuery, controller.signal)])
        .then(([data, nextGraph]) => {
          setCourses(data.courses); setGraph(nextGraph);
          setSelected(previous => previous ? nextGraph.nodes.find(course => course.id === previous.id) || data.courses.find(course => course.id === previous.id) || null : null);
          setLoading(false);
        }).catch(cause => { if (!controller.signal.aborted) { setError(String(cause.message)); setCourses([]); setGraph(EMPTY_GRAPH); setLoading(false); } });
    }, 200);
    return () => { clearTimeout(timer); controller.abort(); };
  }, [meta, programId, supporting, subject, search, focus, retry]);

  const program = programs.find(item => item.id === programId);
  function selectProgram(value: string) {
    setProgramId(value); setSubject(''); setSearch(''); setFocus(''); setSelected(null);
  }

  return <>
    <header className="site-header"><Link className="brand" href="/" aria-label="Lassonde Atlas home"><span className="brand-mark">L<span>↗</span></span><span>Lassonde<span className="brand-light">Atlas</span></span></Link><nav aria-label="Main navigation"><a className="active" href="#explore">Course atlas</a><a href="#sources">Sources & coverage</a></nav><span className="local-badge"><i /> LOCAL RESEARCH BUILD</span></header>
    <main>
      <div className="intro"><div><div className="eyebrow">YOUR DEGREE. THE BIGGER PICTURE.</div><h1>See how it all <em>connects.</em></h1><p>Explore Lassonde courses and trace the paths between them.<br />One source-linked atlas, shaped around your degree.</p></div><div className="calendar-stamp"><span>ACADEMIC CALENDAR</span><strong>2026 — 2027</strong><small>Match your program-entry calendar</small></div></div>
      <div className="coverage-strip"><div><span className="live-dot" /><strong>{meta?.coverage.lassondeDetails ?? '—'}</strong><span>of {meta?.coverage.lassondeIndexed ?? '—'} Lassonde details retrieved</span></div><div><strong>{meta?.coverage.programsExtracted ?? '—'}</strong><span>checklists extracted</span></div><div><strong>12</strong><span>Lassonde subjects</span></div><div className="source-note">Official sources. Automated extraction.<br /><strong>Not an academic eligibility or degree audit.</strong></div></div>
      <section className="explorer" id="explore" aria-label="Course explorer">
        <aside className="filters"><div className="section-kicker">MAKE IT YOURS</div><h2>Find your path</h2><label htmlFor="calendar">Calendar year</label><select id="calendar" value="2026-2027" disabled><option>2026-2027</option></select><p className="field-help">Only this calendar is imported. Historical degrees are not inferred.</p>
          <label htmlFor="degree">Exact degree / stream</label><select id="degree" value={programId} onChange={event => selectProgram(event.target.value)}><option value="">All Lassonde courses</option><optgroup label="Degree and stream checklists">{programs.filter(item => item.kind === 'program').map(item => <option key={item.id} value={item.id}>{item.label}{item.status !== 'references-extracted' ? ' · source only' : ''}</option>)}</optgroup><optgroup label="First-year planning aids">{programs.filter(item => item.kind === 'planning-aid').map(item => <option key={item.id} value={item.id}>{item.label}</option>)}</optgroup></select>
          {program && <div className="degree-note"><strong>{program.status === 'references-extracted' ? 'Degree checklist scope' : 'Not yet extracted'}</strong><p>{program.status === 'references-extracted' ? 'Course-code column entries, including alternatives and elective candidates. Prerequisite-note columns are not degree requirements. Not every node is mandatory.' : 'This format is not supported yet. No degree-specific coverage is claimed.'}</p><a href={program.sourceUrl} target="_blank" rel="noreferrer">Open official checklist ↗</a><details><summary>Original curriculum groups ({program.groups?.length || 0})</summary>{program.groups?.map((group, index) => <p key={index}><strong>{group.yearHeading} · {group.kind}</strong><br />{group.text}<br /><small>{group.sheet}!{group.cell} · unreviewed</small></p>)}</details></div>}
          <label htmlFor="subject">Subject</label><select id="subject" value={subject} onChange={event => { setSubject(event.target.value); setFocus(''); }}><option value="">All subjects in scope</option>{(meta?.coverage.subjects || []).map(item => <option key={item}>{item}</option>)}</select>
          <label htmlFor="search">Search code or title</label><div className="search-field"><span aria-hidden="true">⌕</span><input id="search" type="search" placeholder="e.g. EECS 2030" value={search} onChange={event => { setSearch(event.target.value); setSubject(''); setFocus(''); }} /></div>
          <label className="checkbox"><input type="checkbox" checked={supporting} onChange={event => { setSupporting(event.target.checked); setFocus(''); }} /><span>Include prerequisite connections<small>Keep MATH, PHYS and other supporting references visible.</small></span></label>
          <div className="filter-foot"><span className="tiny-square" /> Start with a subject, choose your exact checklist, or search across all Lassonde courses.</div>
          <button className="text-button" onClick={() => selectProgram('')}>Clear all filters</button>
        </aside>
        <div className="workspace"><div className="workspace-toolbar"><div><span className="section-kicker">THE COURSE ATLAS</span><h2>{focus ? focus + ' connections' : 'Prerequisite reference map'}</h2><p>{loading ? 'Loading source records…' : courses.length + ' matching courses · ' + graph.nodes.length + ' map nodes'}</p></div><div className="view-toggle" role="group" aria-label="Course display"><button aria-pressed={view === 'map'} className={view === 'map' ? 'chosen' : ''} onClick={() => setView('map')}>↗ Map</button><button aria-pressed={view === 'list'} className={view === 'list' ? 'chosen' : ''} onClick={() => setView('list')}>☷ List</button></div></div>
          <div className="map-explainer"><span>ⓘ</span><p>Connections show references, <strong>not “take all of these.”</strong> Alternatives, GPA, permissions and other conditions remain in the original rule text.</p></div>
          {focus && <button className="focus-reset" onClick={() => setFocus('')}>← Back to filtered map</button>}
          {selected && <a className="selection-link" href="#detail-heading">Selected: {selected.id} — view description and original rules ↓</a>}
          {error ? <div className="empty-state" role="alert"><h3>We couldn’t load this scope.</h3><p>{error}</p><button className="primary-button" onClick={() => setRetry(value => value + 1)}>Try again</button></div> : loading ? <div className="empty-state" role="status"><span className="loading-ring" /><h3>Connecting the dots…</h3><p>Reading the local official-source snapshot.</p></div> : !graph.nodes.length ? <div className="empty-state"><h3>No courses in this view.</h3><p>Try another subject, clear your search, or open the official checklist for unsupported formats.</p></div> : view === 'map' ? <PrerequisiteMap graph={graph} selected={selected?.id || ''} onSelect={setSelected} /> : <CourseList graph={graph} selected={selected?.id || ''} onSelect={setSelected} />}
          <div className="map-legend"><span><i className="legend-line" /> Prerequisite reference</span><span><i className="legend-line dashed" /> Corequisite / combined</span><span><i className="legend-node" /> Supporting / unresolved</span><span>Columns are course levels, not recommended years.</span></div>
        </div>
      </section>
      <CourseDetail course={selected} canFocus={!!selected && graph.nodes.some(course => course.id === selected.id)} program={program} onSelect={setSelected} onFocus={identifier => { setFocus(identifier); document.querySelector('#explore')?.scrollIntoView({ behavior: 'smooth' }); }} />
      <section className="sources-section" id="sources"><div><div className="section-kicker">BUILT ON EVIDENCE, NOT ASSUMPTIONS</div><h2>Know what this atlas covers.</h2><p>York’s public academic catalogue and Lassonde’s official checklist files.<br />Locally imported; not a live enrolment or timetable service.</p></div><div className="source-stats"><p><strong>{meta?.coverage.programsExtracted ?? '—'} / {meta?.coverage.programsLinked ?? '—'}</strong> checklist files extracted <small>Includes planning aids, not just distinct degrees.</small></p><p><strong>{meta?.coverage.unresolvedReferences ?? '—'}</strong> unresolved references <small>Kept visible; never treated as unrestricted.</small></p><p><strong>{meta ? new Date(meta.generatedAt).toLocaleDateString('en-CA') : '—'}</strong> local snapshot <small>No automatic refresh or freshness guarantee.</small></p></div>{meta && <ul>{meta.limitations.map(item => <li key={item}>{item}</li>)}</ul>}{!!meta?.coverage.failures.length && <details><summary>{meta.coverage.failures.length} retrieval / extraction failures</summary>{meta.coverage.failures.map((failure, index) => <p key={index}>{failure.source}: {failure.error}</p>)}</details>}</section>
    </main><footer><span>Lassonde Atlas <small>Independent student-planning research.</small></span><span>Not affiliated with York University. Confirm decisions with official advising.</span></footer>
  </>;
}
