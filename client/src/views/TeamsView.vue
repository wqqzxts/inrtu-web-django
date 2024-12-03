<script setup>
import { computed, onBeforeMount, ref } from "vue";
import axios from "axios";
import _ from "lodash";

const teams = ref([]);

const teamToAdd = ref({});
const teamToEdit = ref({});

///////////////////////////////////////////////////////////////////////
async function fetchTeams() {
  const r = await axios.get("/api/teams/");
  teams.value = r.data;
}

async function onTeamAdd() {
  await axios.post("/api/teams/", {
    ...teamToAdd.value,
  });
  fetchTeams();
}

async function onRemoveClick(team) {
  await axios.delete(`/api/teams/${team.id}/`);
  fetchTeams();
}

async function onTeamEditClick(team) {
  teamToEdit.value = { ...team };
}

async function onUpdateTeam() {
  await axios.patch(`/api/teams/${teamToEdit.value.id}/`, {
    ...teamToEdit.value,
  });
  await fetchTeams();
}

onBeforeMount(async () => {
  await fetchTeams();
});
</script>

<template>
  <div class="container-fluid">
    <div class="p-2">
      <form @submit.prevent.stop="onTeamAdd">
        <div class="row">
          <div class="col">
            <div class="form-floating">
              <input
                type="text"
                class="form-control"
                v-model="teamToAdd.name"
                required
              />
              <label for="floatingInput">Название команды</label>
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
        <div v-for="item in teams" class="team-item">
          <div>{{ item.id }}</div>
          <div>{{ item.name }}</div>
          <button
            class="btn btn-outline-info"
            @click="onTeamEditClick(item)"
            data-bs-toggle="modal"
            data-bs-target="#editTeamModal"
          >
            <i class="bi bi-pencil-fill"></i>
          </button>
          <button class="btn btn-outline-danger" @click="onRemoveClick(item)">
            <i class="bi bi-trash-fill"></i>
          </button>
        </div>
      </div>
    </div>

    <div class="modal fade" id="editTeamModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="exampleModalLabel">
              Редактировать команду
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
                    v-model="teamToEdit.name"
                  />
                  <label for="floatingInput">Название команды</label>
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
              @click="onUpdateTeam"
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
.team-item {
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
