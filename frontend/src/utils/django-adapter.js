import axios from "axios"
import CustomStore from 'devextreme/data/custom_store';

/* eslint-disable */
let odataToDjango = {
  "=": "",
  ">=": "__gte",
  "<=": "__lte",
  ">": "__gt",
  "<": "__lt",
  "contains": "__icontains",
  "startswith": "__istartswith",
  "endswith": "__iendswith",
}


function djangoStore(url) {
  const endpoint = axios.create({
    baseURL: url,
    timeout: 5000,
  })


  return new CustomStore({
    key: 'id',
    async load(loadOptions) {
      //console.log(loadOptions)
      let options = `?limit=${loadOptions.take}&offset=${loadOptions.skip}`

      if (loadOptions.searchValue){
        options += "&_search=" + loadOptions.searchValue
      }

      if (loadOptions.sort) {
        let sort = loadOptions.sort.map((o) => { return `${o.desc ? "" : "-"}${o.selector}` })
        options += "&ordering=" + sort.join(",")
      }

      if (loadOptions.filter) {
        function recursiveSearch(elem) {
          // skip strings like "and"
          if (!Array.isArray(elem)) {
            return
          }
          // if nested array call search on each element
          if (elem.some(Array.isArray)) {
            elem.forEach(recursiveSearch)
            return
          }

          let [field, operator, value] = elem;
          operator = odataToDjango[operator] || "";
          options += `&${field}${operator}=${value}`;
        }
        recursiveSearch(loadOptions.filter)
      }
      const response = await endpoint.get("/" + options);
      const result = response.data

      return {
        data: result.results || result,
        totalCount: result.count || result.length,
      };
    },
    async keyOf (elem) {
      return elem.id
    },
    async byKey (key) {
      return await endpoint.get(`/${key}/`)
    },
    async insert(values) {
      await endpoint.post("/", values);
    },
    async update(key, values) {
      await endpoint.patch(`/${key}/`, values);
    },
    async remove(key) {
      await endpoint.delete(`/${key}/`)
    }
  });
}

export default djangoStore