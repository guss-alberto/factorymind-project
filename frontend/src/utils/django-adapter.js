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


function djangoStore(url, key) {
  const endpoint = axios.create({
    baseURL: url,
    timeout: 5000,
  })

  return new CustomStore({
    key: key || "id",
    async load(loadOptions) {
      // console.log(url)
      // console.log(loadOptions)
      let params = {}

      if (loadOptions.take) {
        params.limit = loadOptions.take
        params.offset = loadOptions.skip
      }

      if (loadOptions.searchValue) {
        params._search = loadOptions.searchValue
      }

      if (loadOptions.sort) {
        let sort = loadOptions.sort.map((o) => { return `${o.desc ? "" : "-"}${o.selector}` })
        parms.ordering = sort.join(",")
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
          params[`${field}${operator}`]= value
        }
        recursiveSearch(loadOptions.filter)
      }
      const response = await endpoint.get("/", { params });
      const result = response.data

      return {
        data: result.results || result,
        totalCount: result.count || result.length || 0,
      };
    },
    async keyOf(elem) {
      return elem.id
    },
    async byKey(key) {
      const resp = await endpoint.get(`/${key}/`)
      return resp.data
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