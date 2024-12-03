<script setup>
import { computed, onBeforeMount, ref } from "vue";
import axios from "axios";
import _ from "lodash";

const positions = ref([]);

const positionToAdd = ref({});
const positionToEdit = ref({});

///////////////////////////////////////////////////////////////////////
async function fetchPositions() {
  const r = await axios.get("/api/positions/");
  positions.value = r.data;
}

async function onPositionAdd() {
  await axios.post("/api/positions/", {
    ...positionToAdd.value,
  });
  fetchPositions();
}

async function onRemoveClick(position) {
  await axios.delete(`/api/positions/${position.id}/`);
  fetchPositions();
}

async function onPositionEditClick(position) {
  positionToEdit.value = { ...position };
}

async function onUpdatePosition() {
  await axios.patch(`/api/positions/${positionToEdit.value.id}/`, {
    ...positionToEdit.value,
  });
  await fetchPositions();
}

onBeforeMount(async () => {
  await fetchPositions();
});
</script>

<template>
  <div class="container-fluid">
    <div class="p-2">
      <form @submit.prevent.stop="onPositionAdd">
        <div class="row">
          <div class="col">
            <div class="form-floating">
              <input
                type="text"
                class="form-control"
                v-model="positionToAdd.name"
                required
              />
              <label for="floatingInput">Название роли</label>
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
        <div v-for="item in positions" class="position-item">
          <div>{{ item.id }}</div>
          <div>{{ item.name }}</div>
          <button
            class="btn btn-outline-info"
            @click="onPositionEditClick(item)"
            data-bs-toggle="modal"
            data-bs-target="#editPositionModal"
          >
            <i class="bi bi-pencil-fill"></i>
          </button>
          <button class="btn btn-outline-danger" @click="onRemoveClick(item)">
            <i class="bi bi-trash-fill"></i>
          </button>
        </div>
      </div>
    </div>

    <div class="modal fade" id="editPositionModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="exampleModalLabel">
              Редактировать роль
            </h1>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
            ></button>
          </div>
          <div class="modal-body">
            <div class="row">
              <div class="col">
                <div class="form-floating">
                  <input
                    type="text"
                    class="form-control"
                    v-model="positionToEdit.name"
                  />
                  <label for="floatingInput">Название роли</label>
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
              @click="onUpdatePosition"
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
.position-item {
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
