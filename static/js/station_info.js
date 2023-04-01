const url = window.location.origin + '/api/v1' + window.location.pathname;

fetch(url)
  .then(response => response.json())
  .then(data =>
      d3.select('.station_name')
        .text(data[0].station_name)
  );

// const container = d3.select('.albedo');
//
// // Получаем значения из элементов списка li, кроме первого
// const data = container.selectAll('li:not(:first-child)')
//   .nodes()
//   .map(node => +node.textContent);
//
// // Создаем шкалу для оси x
// const xScale = d3.scaleBand()
//   .domain(d3.range(data.length))
//   .range([0, container.node().clientWidth])
//   .paddingInner(0.05);
//
// // Создаем шкалу для оси y
// const yScale = d3.scaleLinear()
//   .domain([0, d3.max(data)])
//   .range([container.node().clientHeight, 0]);
//
// // Создаем контейнер для графика
// const svg = container.append('svg')
//   .attr('width', 300) // Изменяем размер области отрисовки
//   .attr('height', 200);
//
// // Добавляем ось x
// const xAxis = d3.axisBottom(xScale)
//   .tickSizeInner(-container.node().clientHeight) // Размер внутренних меток оси
//   .tickSizeOuter(0); // Размер внешних меток оси
//
// svg.append('g')
//   .attr('transform', `translate(0, ${container.node().clientHeight})`) // Смещаем ось вниз
//   .call(xAxis);
//
// // Добавляем ось y
// const yAxis = d3.axisLeft(yScale)
//   .tickSizeInner(-container.node().clientWidth) // Размер внутренних меток оси
//   .tickSizeOuter(0); // Размер внешних меток оси
//
// svg.append('g')
//   .call(yAxis);
//
// // Добавляем сетку
// const grid = d3.axisLeft(yScale)
//   .tickSize(-container.node().clientWidth) // Размер линий сетки
//   .tickFormat('');
//
// svg.append('g')
//   .call(grid);
//
// // Добавляем линию графика
// const line = d3.line()
//   .x((d, i) => xScale(i))
//   .y(d => yScale(d));
//
// svg.append('path')
//   .datum(data)
//   .attr('fill', 'none')
//   .attr('stroke', 'steelblue')
//   .attr('stroke-width', 2)
//   .attr('d', line);