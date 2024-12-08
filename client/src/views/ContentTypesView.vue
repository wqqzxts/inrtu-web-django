<script setup>
import { computed, onBeforeMount, ref } from "vue";
import axios from "axios";
import _ from "lodash";

const content_type = ref([]);

const contentTypeToAdd = ref({});
const contentTypeToEdit = ref({});

///////////////////////////////////////////////////////////////////////
async function fetchContentTypes() {
  const r = await axios.get("/api/content-types/");
  content_type.value = r.data;
}

async function onContentTypeAdd() {
  await axios.post("/api/content-types/", {
    ...contentTypeToAdd.value,
  });
  fetchContentTypes();
}

async function onRemoveClick(content_type) {
  await axios.delete(`/api/content-types/${content_type.id}/`);
  fetchContentTypes();
}

async function onContentTypeEditClick(content_type) {
  contentTypeToEdit.value = { ...content_type };
}

async function onUpdateContentType() {
  await axios.patch(`/api/content-types/${contentTypeToEdit.value.id}/`, {
    ...contentTypeToEdit.value,
  });
  await fetchContentTypes();
}

onBeforeMount(async () => {
  await fetchContentTypes();
});
</script>

<template>
  <div class="container-fluid">
    <div class="p-2">
      <form @submit.prevent.stop="onContentTypeAdd">
        <div class="row">
          <div class="col">
            <div class="form-floating">
              <input
                type="text"
                class="form-control"
                v-model="contentTypeToAdd.name"
                required
              />
              <label for="floatingInput">Тип контента</label>
            </div>
          </div>

          <div class="col-auto" style="align-content: center">
            <button class="btn btn-outline-success btn-lg">
              <i class="bi bi-database-fill-add"></i>
            </button>
          </div>
        </div>
      </form>

      <div>
        <div v-for="item in content_type" class="content-type-item" v-bind:key="item">
          <div>{{ item.name }}</div>          
          <button
            class="btn btn-outline-primary"
            @click="onContentTypeEditClick(item)"
            data-bs-toggle="modal"
            data-bs-target="#editContentTypeModal"
          >
            <i class="bi bi-pencil-fill"></i>
          </button>

          <button class="btn btn-outline-danger" @click="onRemoveClick(item)">
            <i class="bi bi-trash-fill"></i>
          </button>
        </div>
      </div>
    </div>

    <div class="modal fade" id="editContentTypeModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="exampleModalLabel">
              Редактировать тип контента
            </h1>            
          </div>
          <div class="modal-body">
            <div class="col">
              <div class="row">
                <div class="col m-1">
                  <div class="form-floating">
                    <input
                      type="text"
                      class="form-control"
                      v-model="contentTypeToEdit.name"
                    />
                    <label for="floatingInput">Тип контента</label>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-outline-danger"
              data-bs-dismiss="modal"
            >
              <i class="bi bi-x-square-fill"></i>
            </button>
            <button
              data-bs-dismiss="modal"
              type="button"
              class="btn btn-outline-success"
              @click="onUpdateContentType"
            >
              <i class="bi bi-floppy2-fill"></i>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.content-type-item {
  padding: 0.5rem;
  margin: 0.5rem 0;
  border: 1px solid silver;
  border-radius: 6px;
  display: grid;
  grid-template-columns: 1fr auto auto auto;
  gap: 16px;
  align-items: center;
  align-content: center;
}
</style>
