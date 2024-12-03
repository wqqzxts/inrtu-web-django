<script setup>
import { computed, onBeforeMount, ref } from "vue";
import axios from "axios";
import _ from "lodash";

const skills = ref([]);

const skillToAdd = ref({});
const skillToEdit = ref({});

///////////////////////////////////////////////////////////////////////
async function fetchSkills() {
  const r = await axios.get("/api/skills/");
  skills.value = r.data;
}

async function onSkillAdd() {
  await axios.post("/api/skills/", {
    ...skillToAdd.value,
  });
  fetchSkills();
}

async function onRemoveClick(skill) {
  await axios.delete(`/api/skills/${skill.id}/`);
  fetchSkills();
}

async function onSkillDescriptionClick(skill) {
  skillToEdit.value = { ...skill };
}

async function onSkillEditClick(skill) {
  skillToEdit.value = { ...skill };
}

async function onUpdateSkill() {
  await axios.patch(`/api/skills/${skillToEdit.value.id}/`, {
    ...skillToEdit.value,
  });
  await fetchSkills();
}

onBeforeMount(async () => {
  await fetchSkills();
});
</script>

<template>
  <div class="container-fluid">
    <div class="p-2">
      <form @submit.prevent.stop="onSkillAdd">
        <div class="row">
          <div class="col">
            <div class="form-floating">
              <input
                type="text"
                class="form-control"
                v-model="skillToAdd.name"
                required
              />
              <label for="floatingInput">Название способности</label>
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
        <div v-for="item in skills" :key="item.name" class="skill-item">
          <div>{{ item.name }}</div>
          <button
            class="btn btn-outline-info"
            @click="onSkillEditClick(item)"
            data-bs-toggle="modal"
            data-bs-target="#descriptionSkillModal"
          >
            <i class="bi bi-three-dots"></i>
          </button>

          <button
            class="btn btn-outline-primary"
            @click="onSkillEditClick(item)"
            data-bs-toggle="modal"
            data-bs-target="#editSkillModal"
          >
            <i class="bi bi-pencil-fill"></i>
          </button>

          <button class="btn btn-outline-danger" @click="onRemoveClick(item)">
            <i class="bi bi-trash-fill"></i>
          </button>
        </div>
      </div>
    </div>

    <div class="modal fade" id="editSkillModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="exampleModalLabel">
              Редактировать способность
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
                    v-model="skillToEdit.name"
                  />
                  <label for="floatingInput">Название способности</label>
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
              @click="onUpdateSkill"
            >
              <i class="bi bi-floppy2-fill"></i>
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="descriptionSkillModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="exampleModalLabel">
              Описание способности
            </h1>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
            ></button>
          </div>
          <div class="modal-body"></div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-outline-danger"
              data-bs-dismiss="modal"
            >
              <i class="bi bi-x-square-fill"></i>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.skill-item {
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
